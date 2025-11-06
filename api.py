"""
API REST PARA PET STORE CHATBOT
Endpoints para integración con frontend React
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from database import PetStoreDatabase
from predictor import PetStorePredictor
from chatbot import PetStoreBot
from transformer_chatbot import PetStoreBotTransformer

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Pet Store Chatbot API",
    description="API REST para chatbot con IA y análisis predictivo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
db = PetStoreDatabase()
predictor = PetStorePredictor()
bot = PetStoreBot()
bot_transformer = PetStoreBotTransformer()

# Intentar cargar modelos entrenados
try:
    predictor.cargar_modelos()
    logger.info("✅ Modelos predictivos cargados exitosamente")
except:
    logger.warning("⚠️ Modelos predictivos no encontrados. Entrena primero.")

# Verificar modelo transformer
if bot_transformer.model_trained:
    logger.info("✅ Chatbot Transformer cargado y listo")
else:
    logger.info("ℹ️  Chatbot usando modo híbrido (sin transformer entrenado)")


# =============================================================================
# MODELOS DE DATOS (Request/Response)
# =============================================================================

class ChatRequest(BaseModel):
    mensaje: str
    usuario_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    respuesta: str
    intencion: str
    confianza: float
    timestamp: str
    modelo: Optional[str] = "Transformer"  # Indica qué modelo generó la respuesta

class PrediccionTipoMascotaRequest(BaseModel):
    dia_semana: int  # 0=Domingo, 1=Lunes, ..., 6=Sábado
    hora: int  # 0-23
    mes: int  # 1-12
    service_id: int

class PrediccionTipoMascotaResponse(BaseModel):
    predicciones: List[Dict[str, Any]]
    tipo_mas_probable: str
    confianza: float

class PrediccionAsistenciaRequest(BaseModel):
    dia_semana: int
    hora: int
    mes: int
    service_id: int
    edad_mascota: int

class PrediccionAsistenciaResponse(BaseModel):
    probabilidad_asistencia: float
    asistira: bool
    confianza: str

class EstadisticasResponse(BaseModel):
    total_mascotas: int
    total_clientes: int
    total_citas: int
    total_servicios: int


# =============================================================================
# ENDPOINTS - INFORMACIÓN GENERAL
# =============================================================================

@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz - Información de la API"""
    return {
        "nombre": "Pet Store Chatbot API",
        "version": "2.0.0",
        "descripcion": "API REST con IA para análisis predictivo, chatbot y métricas de negocio",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "estadisticas": "/api/estadisticas",
            "predicciones": "/api/predicciones",
            "analisis": "/api/analisis",
            "metricas_negocio": "/api/metricas"
        },
        "nuevas_funcionalidades": {
            "version": "2.0.0",
            "fecha": "2024-11-04",
            "metricas_negocio": [
                "Citas del día",
                "Cantidad de productos",
                "Ventas diarias y mensuales",
                "Productos próximos a vencer",
                "Alertas de bajo inventario",
                "Comparativa de ventas mensual",
                "Dashboard consolidado"
            ],
            "chatbot_mejorado": [
                "Análisis de ventas",
                "Consulta de inventario",
                "Alertas de productos",
                "Respuestas sobre métricas de negocio"
            ]
        }
    }

@app.get("/api/health", tags=["General"])
async def health_check():
    """Verifica el estado de la API y conexiones"""
    try:
        stats = db.obtener_estadisticas_generales()
        return {
            "status": "ok",
            "database": "connected",
            "modelos_entrenados": predictor.trained,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error: {str(e)}")


# =============================================================================
# ENDPOINTS - CHATBOT
# =============================================================================

@app.post("/api/chat", response_model=ChatResponse, tags=["Chatbot"])
async def chat(request: ChatRequest, use_transformer: bool = True):
    """
    Envía un mensaje al chatbot y obtiene respuesta usando Red Neuronal Transformer
    
    **Arquitectura Transformer:**
    - Multi-Head Attention para entender contexto
    - Positional Encoding para orden de palabras
    - Feed-Forward Networks para procesamiento profundo
    - Generación autoregresiva de respuestas naturales
    
    **Parámetros:**
    - mensaje: El texto del usuario
    - usuario_id: Identificador del usuario (opcional)
    - use_transformer: True para usar Transformer, False para LSTM clásico (default: True)
    
    **Ejemplo de uso:**
    ```javascript
    const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            mensaje: "¿Cuál es el tipo de mascota más común?",
            usuario_id: "user123"
        })
    });
    const data = await response.json();
    ```
    
    **Ventajas del Transformer:**
    - Respuestas más naturales y contextuales
    - Mejor comprensión del lenguaje
    - Generación dinámica (no solo respuestas predefinidas)
    - Arquitectura estado del arte en NLP
    """
    try:
        if use_transformer:
            # Usar el nuevo chatbot con Transformer
            resultado = bot_transformer.procesar_mensaje(request.mensaje)
            logger.info(f"💬 Transformer generó respuesta con {resultado['confianza']:.0%} confianza")
        else:
            # Usar el chatbot LSTM clásico
            resultado = bot.procesar_mensaje(request.mensaje)
            logger.info(f"💬 LSTM generó respuesta con {resultado['confianza']:.0%} confianza")
        
        return ChatResponse(**resultado)
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/comandos", tags=["Chatbot"])
async def obtener_comandos():
    """Lista todos los comandos disponibles del chatbot"""
    return {
        "comandos": [
            {
                "comando": "estadísticas",
                "descripcion": "Muestra estadísticas generales del sistema",
                "ejemplo": "Muéstrame las estadísticas"
            },
            {
                "comando": "tipo más común",
                "descripcion": "Muestra el tipo de mascota más común",
                "ejemplo": "¿Cuál es el tipo de mascota más común?"
            },
            {
                "comando": "día con más atención",
                "descripcion": "Muestra el día con más citas",
                "ejemplo": "¿Qué día hay más atención?"
            },
            {
                "comando": "servicios",
                "descripcion": "Lista servicios disponibles",
                "ejemplo": "Muéstrame los servicios"
            },
            {
                "comando": "buscar mascota [nombre]",
                "descripcion": "Busca una mascota por nombre",
                "ejemplo": "Buscar mascota Max"
            },
            {
                "comando": "predice tipo mascota",
                "descripcion": "Predice tipo de mascota con IA",
                "ejemplo": "Predice el tipo de mascota"
            }
        ]
    }


# =============================================================================
# ENDPOINTS - ESTADÍSTICAS Y ANÁLISIS
# =============================================================================

@app.get("/api/estadisticas", response_model=EstadisticasResponse, tags=["Estadísticas"])
async def obtener_estadisticas():
    """
    Obtiene estadísticas generales del sistema
    
    **Retorna:**
    - Total de mascotas registradas
    - Total de clientes
    - Total de citas
    - Total de servicios disponibles
    """
    try:
        stats = db.obtener_estadisticas_generales()
        return EstadisticasResponse(**stats)
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analisis/tipos-mascota", tags=["Análisis"])
async def analisis_tipos_mascota():
    """
    Análisis de tipos de mascotas más comunes
    
    **Retorna:**
    - Tipo más común
    - Distribución completa con porcentajes
    - Total de mascotas por tipo
    """
    try:
        df = db.obtener_tipos_mascota_mas_comunes()
        
        if df.empty:
            return {"error": "No hay datos disponibles"}
        
        # Convertir a formato JSON amigable
        tipos = []
        for _, row in df.iterrows():
            tipos.append({
                "tipo_mascota": row['tipo_mascota'],
                "total_mascotas": int(row['total_mascotas']),
                "total_citas": int(row['total_citas']),
                "promedio_citas": float(row['promedio_citas_por_mascota']),
                "porcentaje": float(row['porcentaje'])
            })
        
        return {
            "tipo_mas_comun": tipos[0]['tipo_mascota'] if tipos else None,
            "estadisticas": tipos
        }
    except Exception as e:
        logger.error(f"Error en análisis de tipos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analisis/dias-atencion", tags=["Análisis"])
async def analisis_dias_atencion():
    """
    Análisis de días con más atención
    
    **Retorna:**
    - Día con más citas
    - Distribución semanal completa
    - Tasa de asistencia por día
    """
    try:
        df = db.obtener_dias_con_mas_atencion()
        
        if df.empty:
            return {"error": "No hay datos disponibles"}
        
        dias = []
        for _, row in df.iterrows():
            dias.append({
                "dia_semana": row['dia_semana'],
                "numero_dia": int(row['numero_dia']),
                "total_citas": int(row['total_citas']),
                "completadas": int(row['completadas']),
                "canceladas": int(row['canceladas']),
                "tasa_asistencia": float(row['tasa_asistencia'])
            })
        
        # Ordenar por cantidad de citas
        dias_ordenados = sorted(dias, key=lambda x: x['total_citas'], reverse=True)
        
        return {
            "dia_mas_atencion": dias_ordenados[0]['dia_semana'] if dias_ordenados else None,
            "estadisticas": dias
        }
    except Exception as e:
        logger.error(f"Error en análisis de días: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analisis/horas-pico", tags=["Análisis"])
async def analisis_horas_pico():
    """
    Análisis de horas con más demanda
    
    **Retorna:**
    - Hora pico del día
    - Distribución por hora
    - Mascotas y clientes únicos por hora
    """
    try:
        df = db.obtener_horas_pico()
        
        if df.empty:
            return {"error": "No hay datos disponibles"}
        
        horas = []
        for _, row in df.iterrows():
            horas.append({
                "hora": int(row['hora']),
                "total_citas": int(row['total_citas']),
                "mascotas_unicas": int(row['mascotas_unicas']),
                "clientes_unicos": int(row['clientes_unicos']),
                "duracion_promedio": float(row['duracion_promedio']) if row['duracion_promedio'] else 0
            })
        
        # Ordenar por cantidad de citas
        horas_ordenadas = sorted(horas, key=lambda x: x['total_citas'], reverse=True)
        
        return {
            "hora_pico": horas_ordenadas[0]['hora'] if horas_ordenadas else None,
            "estadisticas": horas[:10]  # Top 10
        }
    except Exception as e:
        logger.error(f"Error en análisis de horas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analisis/servicios", tags=["Análisis"])
async def analisis_servicios():
    """
    Análisis de servicios más utilizados
    
    **Retorna:**
    - Ranking de servicios
    - Total de citas por servicio
    - Tasa de asistencia por servicio
    """
    try:
        df = db.obtener_servicios_mas_utilizados()
        
        if df.empty:
            return {"error": "No hay datos disponibles"}
        
        servicios = []
        for _, row in df.iterrows():
            servicios.append({
                "service_id": int(row['service_id']),
                "servicio": row['servicio'],
                "precio": float(row['precio']),
                "total_citas": int(row['total_citas']),
                "completadas": int(row['completadas']),
                "canceladas": int(row['canceladas']),
                "tasa_asistencia": float(row['tasa_asistencia'])
            })
        
        return {
            "servicio_mas_popular": servicios[0]['servicio'] if servicios else None,
            "estadisticas": servicios
        }
    except Exception as e:
        logger.error(f"Error en análisis de servicios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS - PREDICCIONES CON IA
# =============================================================================

@app.post("/api/predicciones/tipo-mascota", 
         response_model=PrediccionTipoMascotaResponse, 
         tags=["Predicciones"])
async def predecir_tipo_mascota(request: PrediccionTipoMascotaRequest):
    """
    Predice el tipo de mascota más probable usando Red Neuronal
    
    **Parámetros:**
    - dia_semana: 0=Domingo, 1=Lunes, ..., 6=Sábado
    - hora: 0-23
    - mes: 1-12
    - service_id: ID del servicio
    
    **Ejemplo:**
    ```javascript
    const response = await fetch('http://localhost:8000/api/predicciones/tipo-mascota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            dia_semana: 5,  // Viernes
            hora: 10,
            mes: 11,
            service_id: 1
        })
    });
    ```
    """
    if not predictor.trained:
        raise HTTPException(
            status_code=400, 
            detail="Los modelos no están entrenados. Entrena primero usando POST /api/entrenar"
        )
    
    try:
        resultado = predictor.predecir_tipo_mascota(
            request.dia_semana,
            request.hora,
            request.mes,
            request.service_id
        )
        return PrediccionTipoMascotaResponse(**resultado)
    except Exception as e:
        logger.error(f"Error en predicción tipo mascota: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predicciones/asistencia", 
         response_model=PrediccionAsistenciaResponse, 
         tags=["Predicciones"])
async def predecir_asistencia(request: PrediccionAsistenciaRequest):
    """
    Predice la probabilidad de que un cliente asista a una cita
    
    **Parámetros:**
    - dia_semana: 0-6
    - hora: 0-23
    - mes: 1-12
    - service_id: ID del servicio
    - edad_mascota: Edad en años
    
    **Retorna:**
    - Probabilidad de asistencia (0-1)
    - Predicción (asistirá o no)
    - Nivel de confianza
    """
    if not predictor.trained:
        raise HTTPException(
            status_code=400,
            detail="Los modelos no están entrenados"
        )
    
    try:
        resultado = predictor.predecir_asistencia(
            request.dia_semana,
            request.hora,
            request.mes,
            request.service_id,
            request.edad_mascota
        )
        return PrediccionAsistenciaResponse(**resultado)
    except Exception as e:
        logger.error(f"Error en predicción asistencia: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predicciones/tipo-mas-comun", tags=["Predicciones"])
async def obtener_tipo_mas_comun():
    """
    Análisis (no predicción) del tipo de mascota más común en la BD
    
    **Retorna:**
    - Tipo más común
    - Estadísticas completas por tipo
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        analisis = predictor.analizar_tipo_mascota_mas_comun(df)
        return analisis
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predicciones/dia-mas-atencion", tags=["Predicciones"])
async def obtener_dia_mas_atencion():
    """
    Análisis (no predicción) del día con más atención
    
    **Retorna:**
    - Día con más citas
    - Estadísticas semanales
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        analisis = predictor.analizar_dia_mas_atencion(df)
        return analisis
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS - HIERARCHICAL CLUSTERING
# =============================================================================

@app.get("/api/clustering/mascotas", tags=["Clustering"])
async def clustering_mascotas(n_clusters: int = 3):
    """
    Aplica Hierarchical Clustering a las mascotas
    
    Agrupa mascotas por características similares:
    - Edad
    - Tipo de servicios que usan
    - Precio de servicios
    
    **Parámetros:**
    - n_clusters: Número de grupos a generar (default: 3)
    
    **Retorna:**
    - Clusters identificados
    - Características de cada cluster
    - Métrica de calidad (Silhouette Score)
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        resultado = predictor.clustering_mascotas(df, n_clusters)
        
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return resultado
    except Exception as e:
        logger.error(f"Error en clustering de mascotas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clustering/clientes", tags=["Clustering"])
async def clustering_clientes(n_clusters: int = 4):
    """
    Segmentación de clientes con Hierarchical Clustering
    
    Agrupa clientes según:
    - Frecuencia de visitas
    - Gasto total
    - Tasa de asistencia
    
    **Parámetros:**
    - n_clusters: Número de segmentos (default: 4)
    
    **Retorna:**
    - Segmentos de clientes (VIP, Regular, Ocasional, Nuevo)
    - Perfil de cada segmento
    - Valor total por segmento
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        resultado = predictor.clustering_clientes(df, n_clusters)
        
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return resultado
    except Exception as e:
        logger.error(f"Error en clustering de clientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clustering/servicios", tags=["Clustering"])
async def clustering_servicios(n_clusters: int = 3):
    """
    Agrupación de servicios con Hierarchical Clustering
    
    Agrupa servicios según:
    - Frecuencia de uso
    - Horario promedio
    - Tasa de asistencia
    
    **Parámetros:**
    - n_clusters: Número de grupos (default: 3)
    
    **Retorna:**
    - Grupos de servicios
    - Servicios en cada grupo
    - Características del grupo
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        resultado = predictor.clustering_servicios(df, n_clusters)
        
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return resultado
    except Exception as e:
        logger.error(f"Error en clustering de servicios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clustering/completo", tags=["Clustering"])
async def clustering_completo():
    """
    Análisis completo de Hierarchical Clustering
    
    Ejecuta clustering en:
    - Mascotas (3 clusters)
    - Clientes (4 segmentos)
    - Servicios (3 grupos)
    
    **Retorna:**
    - Todos los análisis de clustering
    - Métricas de calidad
    - Recomendaciones estratégicas
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")
        
        resultado = predictor.analisis_clustering_completo(df)
        
        return resultado
    except Exception as e:
        logger.error(f"Error en clustering completo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS - MÉTRICAS DE NEGOCIO Y VENTAS
# =============================================================================

@app.get("/api/metricas/citas-hoy", tags=["Métricas de Negocio"])
async def obtener_citas_hoy():
    """
    Obtiene las citas programadas para hoy
    
    **Retorna:**
    - Lista de citas del día con información completa
    - Mascota, cliente, servicio y horario
    """
    try:
        df = db.obtener_citas_hoy()
        
        if df.empty:
            return {
                "citas": [],
                "total_citas": 0,
                "mensaje": "No hay citas programadas para hoy"
            }
        
        # Convertir fecha_hora a string
        df['fecha_hora'] = df['fecha_hora'].astype(str)
        
        citas = df.to_dict('records')
        
        return {
            "citas": citas,
            "total_citas": len(citas),
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        logger.error(f"Error obteniendo citas de hoy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/cantidad-productos", tags=["Métricas de Negocio"])
async def obtener_cantidad_productos():
    """
    Obtiene la cantidad total de productos en inventario
    
    **Retorna:**
    - Total de productos únicos en el inventario
    """
    try:
        total = db.obtener_cantidad_productos()
        
        return {
            "total_productos": total,
            "mensaje": f"Total de productos en inventario: {total}"
        }
    except Exception as e:
        logger.error(f"Error obteniendo cantidad de productos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/ventas-dia", tags=["Métricas de Negocio"])
async def obtener_ventas_dia():
    """
    Obtiene las ventas del día actual
    
    **Retorna:**
    - Total de ventas del día
    - Cantidad de transacciones
    - Items vendidos
    - Ticket promedio
    """
    try:
        ventas = db.obtener_ventas_dia()
        
        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "total_ventas": ventas['total_ventas'],
            "total_transacciones": ventas['total_transacciones'],
            "total_items_vendidos": ventas['total_items_vendidos'],
            "cantidad_productos": ventas['cantidad_productos'],
            "ticket_promedio": ventas['ticket_promedio']
        }
    except Exception as e:
        logger.error(f"Error obteniendo ventas del día: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/ventas-mes", tags=["Métricas de Negocio"])
async def obtener_ventas_mes():
    """
    Obtiene las ventas del mes actual
    
    **Retorna:**
    - Total de ventas del mes
    - Cantidad de transacciones
    - Items vendidos
    - Ticket promedio
    - Clientes únicos
    """
    try:
        ventas = db.obtener_ventas_mes()
        
        mes_actual = datetime.now().strftime("%B %Y")
        
        return {
            "mes": mes_actual,
            "total_ventas": ventas['total_ventas'],
            "total_transacciones": ventas['total_transacciones'],
            "total_items_vendidos": ventas['total_items_vendidos'],
            "cantidad_productos": ventas['cantidad_productos'],
            "ticket_promedio": ventas['ticket_promedio'],
            "clientes_unicos": ventas['clientes_unicos']
        }
    except Exception as e:
        logger.error(f"Error obteniendo ventas del mes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/productos-proximos-vencer", tags=["Métricas de Negocio"])
async def obtener_productos_proximos_vencer(dias: int = 30):
    """
    Obtiene productos próximos a vencer
    
    **Parámetros:**
    - dias: Días de anticipación para alertar (default: 30)
    
    **Retorna:**
    - Lista de productos próximos a vencer
    - Días hasta vencimiento
    - Stock y valor del inventario
    """
    try:
        df = db.obtener_productos_proximos_vencer(dias)
        
        if df.empty:
            return {
                "productos": [],
                "total_productos": 0,
                "mensaje": f"No hay productos próximos a vencer en los próximos {dias} días"
            }
        
        # Convertir fecha a string
        df['fecha_vencimiento'] = df['fecha_vencimiento'].astype(str)
        
        productos = df.to_dict('records')
        valor_total = df['valor_inventario'].sum()
        
        return {
            "productos": productos,
            "total_productos": len(productos),
            "valor_total_inventario": float(valor_total),
            "dias_anticipacion": dias
        }
    except Exception as e:
        logger.error(f"Error obteniendo productos próximos a vencer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/alerta-bajo-inventario", tags=["Métricas de Negocio"])
async def obtener_alerta_bajo_inventario():
    """
    Obtiene productos con bajo inventario (stock actual < stock mínimo)
    
    **Retorna:**
    - Lista de productos con bajo inventario
    - Unidades faltantes
    - Costo de reposición
    """
    try:
        df = db.obtener_alerta_bajo_inventario()
        
        if df.empty:
            return {
                "productos": [],
                "total_alertas": 0,
                "mensaje": "No hay alertas de bajo inventario"
            }
        
        productos = df.to_dict('records')
        costo_total_reposicion = df['costo_reposicion'].sum()
        
        return {
            "productos": productos,
            "total_alertas": len(productos),
            "costo_total_reposicion": float(costo_total_reposicion)
        }
    except Exception as e:
        logger.error(f"Error obteniendo alertas de inventario: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/comparativa-ventas", tags=["Métricas de Negocio"])
async def obtener_comparativa_ventas():
    """
    Obtiene comparativa de ventas: Mes actual vs mes anterior
    
    **Retorna:**
    - Ventas del mes actual
    - Ventas del mes anterior
    - Diferencia y porcentaje de cambio
    - Tendencia (crecimiento/decrecimiento/estable)
    """
    try:
        comparativa = db.obtener_comparativa_ventas_mensual()
        
        # Determinar emoji según tendencia
        emoji_tendencia = {
            'crecimiento': '📈',
            'decrecimiento': '📉',
            'estable': '➡️',
            'sin_datos': '❓',
            'error': '⚠️'
        }
        
        return {
            "ventas_mes_actual": comparativa['ventas_mes_actual'],
            "ventas_mes_anterior": comparativa['ventas_mes_anterior'],
            "transacciones_mes_actual": comparativa['transacciones_mes_actual'],
            "transacciones_mes_anterior": comparativa['transacciones_mes_anterior'],
            "diferencia_ventas": comparativa['diferencia_ventas'],
            "porcentaje_cambio": comparativa['porcentaje_cambio'],
            "tendencia": comparativa['tendencia'],
            "icono_tendencia": emoji_tendencia.get(comparativa['tendencia'], '➡️'),
            "mensaje": _generar_mensaje_tendencia(comparativa)
        }
    except Exception as e:
        logger.error(f"Error obteniendo comparativa de ventas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _generar_mensaje_tendencia(comparativa: Dict) -> str:
    """Genera mensaje descriptivo de la tendencia"""
    porcentaje = comparativa.get('porcentaje_cambio', 0)
    
    if comparativa['tendencia'] == 'crecimiento':
        return f"Las ventas aumentaron {porcentaje:+.2f}% respecto al mes anterior"
    elif comparativa['tendencia'] == 'decrecimiento':
        return f"Las ventas disminuyeron {abs(porcentaje):.2f}% respecto al mes anterior"
    elif comparativa['tendencia'] == 'estable':
        return f"Las ventas se mantienen estables ({porcentaje:+.2f}%)"
    else:
        return "No hay suficientes datos para comparar"

@app.get("/api/metricas/dashboard", tags=["Métricas de Negocio"])
async def obtener_dashboard_completo():
    """
    Obtiene todas las métricas de negocio en una sola llamada
    
    **Retorna:**
    - Citas de hoy
    - Cantidad de productos
    - Ventas del día
    - Ventas del mes
    - Productos próximos a vencer
    - Alertas de bajo inventario
    - Comparativa de ventas mensual
    """
    try:
        # Obtener todas las métricas
        citas_hoy = db.obtener_citas_hoy()
        cantidad_productos = db.obtener_cantidad_productos()
        ventas_dia = db.obtener_ventas_dia()
        ventas_mes = db.obtener_ventas_mes()
        productos_vencer = db.obtener_productos_proximos_vencer(30)
        bajo_inventario = db.obtener_alerta_bajo_inventario()
        comparativa = db.obtener_comparativa_ventas_mensual()
        
        return {
            "citas_hoy": {
                "total": len(citas_hoy),
                "proxima_cita": citas_hoy.iloc[0].to_dict() if not citas_hoy.empty else None
            },
            "productos": {
                "total": cantidad_productos
            },
            "ventas_dia": ventas_dia,
            "ventas_mes": ventas_mes,
            "productos_proximos_vencer": {
                "total": len(productos_vencer),
                "criticos": len(productos_vencer[productos_vencer['dias_hasta_vencer'] <= 7]) if not productos_vencer.empty else 0
            },
            "bajo_inventario": {
                "total_alertas": len(bajo_inventario)
            },
            "comparativa_ventas": {
                "porcentaje_cambio": comparativa['porcentaje_cambio'],
                "tendencia": comparativa['tendencia']
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error obteniendo dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS - CONSULTAS A BASE DE DATOS
# =============================================================================

@app.get("/api/mascotas/buscar/{nombre}", tags=["Consultas"])
async def buscar_mascota(nombre: str):
    """
    Busca mascotas por nombre
    
    **Parámetros:**
    - nombre: Nombre de la mascota (parcial o completo)
    
    **Ejemplo:** `/api/mascotas/buscar/Max`
    """
    try:
        df = db.buscar_mascota_por_nombre(nombre)
        
        if df.empty:
            return {"mascotas": [], "mensaje": f"No se encontró '{nombre}'"}
        
        mascotas = df.to_dict('records')
        return {"mascotas": mascotas, "total": len(mascotas)}
    except Exception as e:
        logger.error(f"Error buscando mascota: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mascotas/{pet_id}/historial", tags=["Consultas"])
async def obtener_historial(pet_id: int):
    """
    Obtiene el historial médico de una mascota
    
    **Parámetros:**
    - pet_id: ID de la mascota
    """
    try:
        df = db.obtener_historial_mascota(pet_id)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No se encontró historial")
        
        historial = df.to_dict('records')
        return {"pet_id": pet_id, "historial": historial}
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mascotas/{pet_id}/citas", tags=["Consultas"])
async def obtener_citas_mascota(pet_id: int):
    """
    Obtiene las próximas citas de una mascota
    
    **Parámetros:**
    - pet_id: ID de la mascota
    """
    try:
        df = db.obtener_proximas_citas_mascota(pet_id)
        
        if df.empty:
            return {"pet_id": pet_id, "citas": [], "mensaje": "No hay citas programadas"}
        
        citas = df.to_dict('records')
        return {"pet_id": pet_id, "citas": citas}
    except Exception as e:
        logger.error(f"Error obteniendo citas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mascotas/{pet_id}/vacunas", tags=["Consultas"])
async def obtener_vacunas(pet_id: int):
    """
    Obtiene el historial de vacunación de una mascota
    
    **Parámetros:**
    - pet_id: ID de la mascota
    """
    try:
        df = db.obtener_vacunas_mascota(pet_id)
        
        if df.empty:
            return {"pet_id": pet_id, "vacunas": [], "mensaje": "No hay vacunas registradas"}
        
        vacunas = df.to_dict('records')
        return {"pet_id": pet_id, "vacunas": vacunas}
    except Exception as e:
        logger.error(f"Error obteniendo vacunas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clientes/buscar/{correo}", tags=["Consultas"])
async def buscar_cliente(correo: str):
    """
    Busca un cliente por correo electrónico
    
    **Parámetros:**
    - correo: Email del cliente
    """
    try:
        df = db.buscar_cliente_por_correo(correo)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        cliente = df.to_dict('records')[0]
        return {"cliente": cliente}
    except Exception as e:
        logger.error(f"Error buscando cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clientes/{client_id}/mascotas", tags=["Consultas"])
async def obtener_mascotas_cliente(client_id: int):
    """
    Obtiene todas las mascotas de un cliente
    
    **Parámetros:**
    - client_id: ID del cliente
    """
    try:
        df = db.obtener_mascotas_cliente(client_id)
        
        if df.empty:
            return {"client_id": client_id, "mascotas": [], "mensaje": "Sin mascotas"}
        
        mascotas = df.to_dict('records')
        return {"client_id": client_id, "mascotas": mascotas, "total": len(mascotas)}
    except Exception as e:
        logger.error(f"Error obteniendo mascotas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/servicios", tags=["Consultas"])
async def obtener_servicios():
    """
    Lista todos los servicios disponibles
    
    **Retorna:**
    - Lista completa de servicios
    - Precio y duración de cada uno
    """
    try:
        df = db.obtener_servicios_disponibles()
        
        if df.empty:
            return {"servicios": [], "mensaje": "No hay servicios disponibles"}
        
        servicios = df.to_dict('records')
        return {"servicios": servicios, "total": len(servicios)}
    except Exception as e:
        logger.error(f"Error obteniendo servicios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS - ENTRENAMIENTO DE MODELOS
# =============================================================================

@app.post("/api/entrenar", tags=["Administración"])
async def entrenar_modelos(background_tasks: BackgroundTasks):
    """
    Entrena los modelos de red neuronal en segundo plano
    
    **ADVERTENCIA:** Este proceso puede tardar 5-10 minutos
    
    **Retorna:**
    - Confirmación de que el entrenamiento ha iniciado
    - El entrenamiento se ejecuta en background
    """
    def entrenar():
        try:
            logger.info("🚀 Iniciando entrenamiento de modelos...")
            
            # Obtener datos
            df = db.obtener_dataset_completo()
            
            if df.empty:
                logger.error("❌ No hay datos para entrenar")
                return
            
            # Entrenar modelos
            predictor.entrenar_modelo_tipo_mascota(df)
            predictor.entrenar_modelo_asistencia(df)
            
            # Guardar modelos
            predictor.guardar_modelos()
            
            logger.info("✅ Entrenamiento completado")
            
        except Exception as e:
            logger.error(f"❌ Error en entrenamiento: {e}")
    
    # Ejecutar en background
    background_tasks.add_task(entrenar)
    
    return {
        "mensaje": "Entrenamiento iniciado en segundo plano",
        "tiempo_estimado": "5-10 minutos",
        "nota": "Verifica el estado con GET /api/predicciones/estado"
    }

@app.get("/api/predicciones/estado", tags=["Administración"])
async def estado_modelos():
    """
    Verifica si los modelos están entrenados y listos
    
    **Retorna:**
    - Estado de los modelos (entrenados o no)
    - Información de archivos de modelos
    """
    import os
    from config import PATHS
    
    modelos_existentes = {
        "predictor_model": os.path.exists(PATHS['predictor_model']),
        "scaler": os.path.exists(PATHS['scaler']),
    }
    
    return {
        "modelos_entrenados": predictor.trained,
        "archivos_modelos": modelos_existentes,
        "todos_listos": all(modelos_existentes.values())
    }


# =============================================================================
# EXPORTACIÓN DE DATOS
# =============================================================================

@app.get("/api/exportar/dataset", tags=["Exportación"])
async def exportar_dataset():
    """
    Exporta el dataset completo para análisis externo
    
    **Retorna:**
    - Dataset en formato JSON
    - Incluye todas las citas con información de mascotas y servicios
    """
    try:
        df = db.obtener_dataset_completo()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos")
        
        # Convertir fechas a string
        df['fecha_cita'] = df['fecha_cita'].astype(str)
        
        dataset = df.to_dict('records')
        
        return {
            "dataset": dataset,
            "total_registros": len(dataset),
            "columnas": list(df.columns)
        }
    except Exception as e:
        logger.error(f"Error exportando dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# MANEJO DE ERRORES
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Recurso no encontrado",
        "detail": str(exc.detail) if hasattr(exc, 'detail') else "Not found",
        "path": str(request.url)
    }

@app.exception_handler(500)
async def server_error_handler(request, exc):
    logger.error(f"Error 500: {exc}")
    return {
        "error": "Error interno del servidor",
        "detail": "Ocurrió un error procesando la solicitud"
    }


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 80)
    print("🚀 INICIANDO API REST - PET STORE CHATBOT")
    print("=" * 80)
    print("\n🌐 Servidor corriendo en: http://localhost:8000")
    print("\n📝 Documentación:")
    print("   • Swagger UI (Recomendado): http://localhost:8000/docs")
    print("   • ReDoc:                    http://localhost:8000/redoc")
    print("\n🔌 Endpoints para Frontend:")
    print("   • Chatbot:       POST   /api/chat")
    print("   • Estadísticas:  GET    /api/estadisticas")
    print("   • Análisis:      GET    /api/analisis/tipos-mascota")
    print("   • Predicciones:  POST   /api/predicciones/tipo-mascota")
    print("   • Buscar:        GET    /api/mascotas/buscar/{nombre}")
    print("   • Servicios:     GET    /api/servicios")
    print("\n💡 Tip: Abre http://localhost:8000/docs para ver todos los endpoints")
    print("\n" + "=" * 80)
    print("✅ LISTO - Presiona Ctrl+C para detener")
    print("=" * 80 + "\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

