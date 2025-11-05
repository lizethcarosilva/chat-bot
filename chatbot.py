"""
CHATBOT VETERINARIO INTELIGENTE CON RED NEURONAL LSTM
Responde preguntas sobre enfermedades, cuidados, vacunas y análisis de datos
"""

import re
import random
import pickle
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
from database import PetStoreDatabase
from predictor import PetStorePredictor
import logging
import os

# Configurar TensorFlow para no mostrar warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PetStoreBot:
    """
    Chatbot veterinario inteligente con red neuronal LSTM
    
    Capacidades:
    - Responder preguntas sobre enfermedades, síntomas, cuidados
    - Información sobre vacunas y desparasitación
    - Consejos de alimentación y comportamiento
    - Análisis de estadísticas de la base de datos
    - Predicciones con red neuronal para análisis de datos
    
    Red Neuronal:
    - Arquitectura: Embedding → Bidirectional LSTM → Dense → Softmax
    - Entrenada con datos veterinarios
    - Clasifica intenciones del usuario
    """
    
    def __init__(self):
        self.db = PetStoreDatabase()
        self.predictor = PetStorePredictor()
        self.nombre_bot = "VetBot 🐾"
        self.contexto = {}
        
        # Variables para red neuronal del chatbot
        self.chatbot_model = None
        self.tokenizer = None
        self.label_encoder = None
        self.intents = {}
        self.max_len = 50
        self.confidence_threshold = 0.6
        
        # Intentar cargar modelo del chatbot veterinario
        try:
            self.cargar_modelo_chatbot()
            logger.info("✓ Chatbot veterinario cargado")
        except Exception as e:
            logger.warning(f"⚠️  Modelo de chatbot no encontrado: {e}")
            logger.warning("   Ejecuta: python entrenar_chatbot_veterinario.py")
        
        # Intentar cargar modelos de predicción de datos
        try:
            self.predictor.cargar_modelos()
            logger.info("✓ Modelos predictivos de datos cargados")
        except:
            logger.warning("⚠️  Modelos predictivos no encontrados.")
    
    def cargar_modelo_chatbot(self):
        """Carga el modelo de red neuronal entrenado para el chatbot"""
        # Cargar modelo
        self.chatbot_model = load_model('models/chatbot_veterinario.h5')
        
        # Cargar tokenizer
        with open('models/tokenizer_veterinario.pkl', 'rb') as f:
            self.tokenizer = pickle.load(f)
        
        # Cargar label encoder
        with open('models/label_encoder_veterinario.pkl', 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        # Cargar intenciones y respuestas
        with open('models/intents_veterinario.pkl', 'rb') as f:
            self.intents = pickle.load(f)
    
    # =========================================================================
    # PROCESAMIENTO DE TEXTO
    # =========================================================================
    
    def normalizar_texto(self, texto: str) -> str:
        """Normaliza el texto de entrada"""
        texto = texto.lower().strip()
        
        # Eliminar signos de puntuación pero mantener letras con acento
        texto = re.sub(r'[^a-záéíóúñü\s0-9]', '', texto)
        
        # Quitar acentos para mejor coincidencia
        acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
        for acento, sin_acento in acentos.items():
            texto = texto.replace(acento, sin_acento)
        
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        return texto
    
    def predecir_intencion_neuronal(self, texto: str) -> Tuple[str, float]:
        """
        Usa la red neuronal para predecir la intención del usuario
        
        Proceso:
        1. Normaliza el texto
        2. Tokeniza (convierte palabras a números)
        3. Padding (rellena/trunca la secuencia)
        4. Pasa por la red neuronal
        5. Obtiene la intención con mayor probabilidad
        
        Returns:
            Tuple (intención, confianza)
        """
        if self.chatbot_model is None:
            return "desconocido", 0.0
        
        # Normalizar
        texto_norm = self.normalizar_texto(texto)
        
        # Tokenizar y convertir a secuencia
        sequence = self.tokenizer.texts_to_sequences([texto_norm])
        
        # Padding
        padded = pad_sequences(sequence, maxlen=self.max_len, padding='post')
        
        # Predecir con la red neuronal
        prediction = self.chatbot_model.predict(padded, verbose=0)[0]
        
        # Obtener clase con mayor probabilidad
        max_confidence = float(np.max(prediction))
        predicted_class = np.argmax(prediction)
        
        # Si la confianza es muy baja, marcar como desconocido
        if max_confidence < self.confidence_threshold:
            return "desconocido", max_confidence
        
        # Convertir índice a etiqueta
        intent = self.label_encoder.inverse_transform([predicted_class])[0]
        
        return intent, max_confidence
    
    def detectar_intencion(self, texto: str) -> str:
        """Detecta la intención del usuario"""
        texto_norm = self.normalizar_texto(texto)
        
        # Saludos
        if any(palabra in texto_norm for palabra in ['hola', 'buenos', 'buenas', 'hey', 'saludos']):
            return 'saludo'
        
        # Despedidas
        if any(palabra in texto_norm for palabra in ['adios', 'chao', 'hasta luego', 'bye']):
            return 'despedida'
        
        # === PRIORIDAD: PREGUNTAS DE NEGOCIO (antes de síntomas) ===
        
        # Estadísticas (con y sin acento, todas las variaciones)
        if any(palabra in texto_norm for palabra in ['estadistica', 'estadisticas', 'estadisticas', 'metricas', 'reporte', 'resumen', 'numeros', 'cifras']):
            return 'estadisticas'
        
        # Clientes (detectar variaciones)
        if 'clientes' in texto_norm or 'cliente' in texto_norm:
            if any(palabra in texto_norm for palabra in ['cuantos', 'cuantas', 'total', 'tengo', 'hay', 'numero']):
                return 'estadisticas'
        
        # Productos próximos a vencer
        if any(palabra in texto_norm for palabra in ['productos', 'producto']) and any(palabra in texto_norm for palabra in ['vencer', 'vencimiento', 'proximos', 'expiran', 'caducan']):
            return 'alertas'
        
        # === INTENCIONES VETERINARIAS (FALLBACK) ===
        
        # Preguntas directas sobre síntomas (NUEVO)
        if any(palabra in texto_norm for palabra in ['sintomas', 'sintoma', 'enfermedad', 'enfermedades', 'que enfermedad', 'como saber']):
            return 'sintomas_enfermedad'
        
        # Síntomas y enfermedades (detección por palabras clave)
        sintomas_palabras = ['fiebre', 'vomito', 'diarrea', 'tos', 'estornuda', 'sangre', 
                            'dolor', 'hinchado', 'inflamado', 'rascando', 'rojo', 'herida',
                            'cojea', 'temblor', 'convulsion', 'debil', 'letargo', 'apetito',
                            'ojos', 'oido', 'oreja', 'piel', 'pelo', 'bulto', 'tumor']
        if any(palabra in texto_norm for palabra in sintomas_palabras):
            return 'sintomas_enfermedad'
        
        # Palabras que indican una consulta médica
        consulta_medica = ['mi perro', 'mi gato', 'mi mascota', 'mi cachorro', 'mi gatito',
                          'esta enfermo', 'esta mal', 'no come', 'no quiere', 'le duele',
                          'tiene', 'presenta', 'sintomas']
        if any(palabra in texto_norm for palabra in consulta_medica):
            # Si menciona mascota y algún síntoma/problema
            if any(s in texto_norm for s in ['tiene', 'esta', 'presenta', 'le', 'se', 'no']):
                return 'consulta_veterinaria'
        
        # Vacunas (MEJORADO)
        if any(palabra in texto_norm for palabra in ['vacuna', 'vacunas', 'vacunar', 'inmunizacion', 'inyeccion', 'calendario vacunacion', 'vacunacion']):
            return 'vacunas'
        
        # Enfermedades específicas (del JSON)
        if any(palabra in texto_norm for palabra in ['parvovirus', 'parvo', 'parvoviral']):
            return 'parvovirus'
        
        if any(palabra in texto_norm for palabra in ['moquillo', 'distemper']):
            return 'moquillo'
        
        if any(palabra in texto_norm for palabra in ['rabia', 'rabioso', 'hidrofobia']):
            return 'rabia'
        
        if any(palabra in texto_norm for palabra in ['leucemia felina', 'felv', 'leucemia']):
            return 'leucemia_felina'
        
        # Desparasitación (MEJORADO)
        if any(palabra in texto_norm for palabra in ['desparasitar', 'desparasitacion', 'parasito', 'parasitos', 'gusano', 'gusanos', 'pulga', 'pulgas', 'garrapata', 'garrapatas', 'desparasitante', 'calendario de desparasitacion', 'calendario desparasitacion']):
            return 'desparasitacion'
        
        # Alimentación (MEJORADO)
        if any(palabra in texto_norm for palabra in ['alimentacion', 'alimentacion adecuada', 'comida', 'comer', 'dieta', 'alimento', 'alimentos', 'que come', 'que dar de comer', 'alimentar']):
            return 'alimentacion'
        
        # Cuidados generales (MEJORADO)
        if any(palabra in texto_norm for palabra in ['cuidado', 'cuidados', 'cuidar', 'bano', 'higiene', 'ejercicio', 'cuidados generales', 'cuidados basicos', 'como cuidar']):
            return 'cuidados'
        
        # Emergencia
        if any(palabra in texto_norm for palabra in ['emergencia', 'urgente', 'grave', 'rapido', 'ayuda']):
            return 'emergencia'
        
        # === INTENCIONES DE DATOS Y SISTEMA ===
        
        # Buscar mascota
        if any(palabra in texto_norm for palabra in ['buscar mascota', 'encontrar mascota', 'mascota llamada', 'buscar', 'encontrar']):
            return 'buscar_mascota'
        
        # Historial
        if any(palabra in texto_norm for palabra in ['historial', 'historia medica', 'registro medico', 'historia', 'registro']):
            return 'historial'
        
        # Servicios
        if any(palabra in texto_norm for palabra in ['servicios', 'servicio', 'que servicios', 'lista de servicios', 'cuales servicios', 'tipos de servicio']):
            return 'servicios'
        
        # === ANÁLISIS ESPECÍFICOS (ANTES de predicciones genéricas) ===
        
        # Tipo de mascota más común (PRIORIDAD)
        if 'tipo' in texto_norm and 'mascota' in texto_norm:
            return 'tipo_mas_comun'
        if 'mascota' in texto_norm and any(palabra in texto_norm for palabra in ['comun', 'mas comun', 'frecuente', 'popular']):
            return 'tipo_mas_comun'
        if any(palabra in texto_norm for palabra in ['cual es el tipo', 'que tipo es mas', 'tipo mas comun']):
            return 'tipo_mas_comun'
        
        # Día con más atención (PRIORIDAD)
        if 'dia' in texto_norm and 'atencion' in texto_norm:
            return 'dia_mas_atencion'
        if 'dia' in texto_norm and 'citas' in texto_norm and 'mas' in texto_norm:
            return 'dia_mas_atencion'
        if any(palabra in texto_norm for palabra in ['que dia hay mas', 'cual dia mas', 'mejor dia']):
            return 'dia_mas_atencion'
        
        # Citas de hoy (PRIORIDAD - pero no si pregunta por día con MÁS)
        if 'citas' in texto_norm and 'hoy' in texto_norm:
            return 'citas_hoy'
        if 'cuantas citas' in texto_norm and 'hoy' in texto_norm:
            return 'citas_hoy'
        
        # === PREDICCIONES Y CLUSTERING (después de análisis específicos) ===
        
        # Predicciones (sin "que tipo" para evitar conflictos)
        if any(palabra in texto_norm for palabra in ['predice', 'prediccion', 'predicciones', 'pronostico', 'predecir']):
            return 'prediccion'
        
        # Clustering
        if any(palabra in texto_norm for palabra in ['clustering', 'cluster', 'agrupar', 'segmentar', 'segmentacion', 'grupos', 'jerarquico']):
            return 'clustering'
        
        # Entrenar modelos
        if any(palabra in texto_norm for palabra in ['entrenar', 'entrenamiento', 'entrenar modelos', 'entrenar ia']):
            return 'entrenar'
        
        # === MÉTRICAS DE NEGOCIO ===
        
        # Ventas
        if any(palabra in texto_norm for palabra in ['ventas', 'venta', 'cuanto vendimos', 'transacciones', 'transaccion']):
            return 'ventas'
        
        # Productos e Inventario
        if any(palabra in texto_norm for palabra in ['productos', 'producto', 'inventario', 'stock']):
            return 'productos'
        
        # Alertas
        if any(palabra in texto_norm for palabra in ['alerta', 'alertas', 'vencimiento', 'vencer']):
            return 'alertas'
        
        # Ayuda
        if any(palabra in texto_norm for palabra in ['ayuda', 'help', 'que puedes', 'comandos']):
            return 'ayuda'
        
        return 'desconocido'
    
    # =========================================================================
    # RESPUESTAS POR INTENCIÓN
    # =========================================================================
    
    def responder_saludo(self) -> str:
        """Responde a saludos"""
        respuestas = [
            "¡Hola! 👋 Soy PetBot, tu asistente virtual del Pet Store. ¿En qué puedo ayudarte?",
            "¡Bienvenido! 🐾 Estoy aquí para ayudarte con información sobre mascotas, servicios y análisis predictivos.",
            "¡Hola! 😊 Pregúntame sobre mascotas, citas, estadísticas o predicciones."
        ]
        return random.choice(respuestas)
    
    def responder_despedida(self) -> str:
        """Responde a despedidas"""
        respuestas = [
            "¡Hasta pronto! 👋 Cuida bien a tus mascotas 🐾",
            "¡Adiós! 😊 Que tengas un excelente día con tus peluditos",
            "¡Nos vemos! 🐕 Regresa cuando necesites ayuda"
        ]
        return random.choice(respuestas)
    
    def responder_ayuda(self) -> str:
        """Muestra comandos disponibles"""
        return """
🤖 **PetBot - Comandos Disponibles:**

📊 **ESTADÍSTICAS Y ANÁLISIS:**
• "estadísticas" - Estadísticas generales del sistema
• "tipo más común" - Tipo de mascota más común
• "día con más atención" - Día con más citas

💼 **MÉTRICAS DE NEGOCIO:**
• "citas hoy" - Citas programadas para hoy
• "ventas" - Reporte de ventas del día y mes
• "alertas" - Alertas de inventario

🔬 **CLUSTERING (Machine Learning):**
• "clustering" - Análisis de agrupamiento jerárquico
• "segmentar clientes" - Segmentación de clientes
• "agrupar mascotas" - Clusters de mascotas

🔮 **PREDICCIONES (Red Neuronal):**
• "predice tipo mascota" - Predicción con IA
• "entrenar" - Información de entrenamiento

Ejemplos:
"¿Cuántas citas hay hoy?"
"Clustering de clientes"
"¿Hay productos próximos a vencer?"
"""
    
    def responder_servicios(self) -> str:
        """Lista servicios disponibles"""
        df = self.db.obtener_servicios_disponibles()
        
        if df.empty:
            return "❌ No se encontraron servicios disponibles."
        
        respuesta = "🏥 **SERVICIOS DISPONIBLES:**\n\n"
        for idx, row in df.head(10).iterrows():
            respuesta += f"• **{row['nombre']}**\n"
            if row['descripcion']:
                respuesta += f"  {row['descripcion']}\n"
            respuesta += f"  💰 Precio: ${row['precio']:,.2f}"
            if row['duracion_minutos']:
                respuesta += f" | ⏱️ Duración: {row['duracion_minutos']} min"
            respuesta += "\n\n"
        
        return respuesta
    
    def responder_estadisticas(self) -> str:
        """Muestra estadísticas generales"""
        stats = self.db.obtener_estadisticas_generales()
        
        respuesta = "📊 **ESTADÍSTICAS GENERALES:**\n\n"
        respuesta += f"🐾 Mascotas registradas: **{stats['total_mascotas']}**\n"
        respuesta += f"👥 Clientes registrados: **{stats['total_clientes']}**\n"
        respuesta += f"📅 Total de citas: **{stats['total_citas']}**\n"
        respuesta += f"🏥 Servicios disponibles: **{stats['total_servicios']}**\n"
        
        return respuesta
    
    def responder_tipo_mas_comun(self) -> str:
        """Responde sobre el tipo de mascota más común"""
        df = self.db.obtener_dataset_completo()
        
        if df.empty:
            return "❌ No hay datos suficientes para realizar el análisis."
        
        analisis = self.predictor.analizar_tipo_mascota_mas_comun(df)
        
        respuesta = f"🐾 **ANÁLISIS: Tipo de Mascota Más Común**\n\n"
        respuesta += f"🏆 El tipo más común es: **{analisis['tipo_mas_comun']}**\n\n"
        respuesta += "📊 **Distribución completa:**\n"
        
        for stat in analisis['estadisticas'][:5]:
            barra = "█" * int(stat['porcentaje'] / 5)
            respuesta += f"• {stat['tipo']}: {stat['cantidad']} ({stat['porcentaje']}%) {barra}\n"
        
        return respuesta
    
    def responder_dia_mas_atencion(self) -> str:
        """Responde sobre el día con más atención"""
        df = self.db.obtener_dataset_completo()
        
        if df.empty:
            return "❌ No hay datos suficientes para realizar el análisis."
        
        analisis = self.predictor.analizar_dia_mas_atencion(df)
        
        respuesta = f"📅 **ANÁLISIS: Día con Más Atención**\n\n"
        respuesta += f"🏆 El día con más citas es: **{analisis['dia_con_mas_atencion']}**\n\n"
        respuesta += "📊 **Distribución semanal:**\n"
        
        for stat in analisis['estadisticas']:
            barra = "█" * (stat['cantidad_citas'] // 10)
            respuesta += f"• {stat['dia']}: {stat['cantidad_citas']} citas {barra}\n"
        
        # Obtener hora pico también
        analisis_hora = self.predictor.analizar_hora_pico(df)
        respuesta += f"\n⏰ **Hora pico:** {analisis_hora['hora_pico']}:00 horas"
        
        return respuesta
    
    def responder_prediccion_tipo(self, dia: int = None, hora: int = None) -> str:
        """Predice tipo de mascota"""
        if not self.predictor.trained:
            return "⚠️ Los modelos aún no están entrenados. Usa el comando 'entrenar' primero."
        
        # Usar valores actuales si no se proporcionan
        ahora = datetime.now()
        dia_semana = dia if dia is not None else ahora.weekday() + 1  # Ajustar formato
        hora_dia = hora if hora is not None else ahora.hour
        mes = ahora.month
        service_id = 1  # Servicio por defecto
        
        prediccion = self.predictor.predecir_tipo_mascota(
            dia_semana % 7, hora_dia, mes, service_id
        )
        
        dias_nombre = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        
        respuesta = f"🔮 **PREDICCIÓN: Tipo de Mascota**\n\n"
        respuesta += f"📅 Día: {dias_nombre[dia_semana % 7]}\n"
        respuesta += f"⏰ Hora: {hora_dia}:00\n\n"
        respuesta += f"🏆 **Predicción:** {prediccion['tipo_mas_probable']}\n"
        respuesta += f"📊 **Confianza:** {prediccion['confianza']:.1%}\n\n"
        respuesta += "**Top 3 más probables:**\n"
        
        for pred in prediccion['predicciones']:
            respuesta += f"• {pred['tipo_mascota']}: {pred['probabilidad']:.1%}\n"
        
        return respuesta
    
    def responder_buscar_mascota(self, nombre: str) -> str:
        """Busca una mascota por nombre"""
        if not nombre:
            return "❓ Por favor proporciona el nombre de la mascota. Ej: 'buscar mascota Max'"
        
        df = self.db.buscar_mascota_por_nombre(nombre)
        
        if df.empty:
            return f"❌ No se encontró ninguna mascota con el nombre '{nombre}'."
        
        respuesta = f"🔍 **RESULTADOS DE BÚSQUEDA: '{nombre}'**\n\n"
        
        for idx, row in df.iterrows():
            respuesta += f"🐾 **{row['nombre']}** (ID: {row['pet_id']})\n"
            respuesta += f"   • Tipo: {row['tipo']}\n"
            respuesta += f"   • Raza: {row['raza']}\n"
            respuesta += f"   • Edad: {row['edad']} años | Sexo: {row['sexo']}\n"
            respuesta += f"   • Propietario: {row['propietario']}\n"
            respuesta += f"   • Contacto: {row['telefono']}\n\n"
        
        return respuesta
    
    def responder_citas_hoy(self) -> str:
        """Muestra las citas programadas para hoy"""
        df = self.db.obtener_citas_hoy()
        
        if df.empty:
            return "✅ No hay citas programadas para hoy."
        
        respuesta = f"📅 **CITAS PROGRAMADAS HOY ({datetime.now().strftime('%d/%m/%Y')})**\n\n"
        respuesta += f"**Total de citas:** {len(df)}\n\n"
        
        for idx, row in df.head(10).iterrows():
            hora = f"{int(row['hora']):02d}:00"
            respuesta += f"🕐 **{hora}** - {row['mascota']} ({row['tipo_mascota']})\n"
            respuesta += f"   • Cliente: {row['cliente']}\n"
            respuesta += f"   • Servicio: {row['servicio']} (${row['precio']:.2f})\n"
            respuesta += f"   • Estado: {row['estado']}\n"
            if row['veterinario']:
                respuesta += f"   • Veterinario: {row['veterinario']}\n"
            respuesta += "\n"
        
        if len(df) > 10:
            respuesta += f"... y {len(df) - 10} citas más.\n"
        
        return respuesta
    
    def responder_ventas(self) -> str:
        """Muestra información de ventas"""
        ventas_dia = self.db.obtener_ventas_dia()
        ventas_mes = self.db.obtener_ventas_mes()
        comparativa = self.db.obtener_comparativa_ventas_mensual()
        
        respuesta = "💰 **REPORTE DE VENTAS**\n\n"
        
        # Ventas del día
        respuesta += "📊 **Ventas del Día:**\n"
        respuesta += f"   • Total: ${ventas_dia['total_ventas']:,.2f}\n"
        respuesta += f"   • Transacciones: {ventas_dia['total_transacciones']}\n"
        respuesta += f"   • Items vendidos: {ventas_dia['total_items_vendidos']}\n"
        respuesta += f"   • Ticket promedio: ${ventas_dia['ticket_promedio']:,.2f}\n\n"
        
        # Ventas del mes
        respuesta += "📅 **Ventas del Mes:**\n"
        respuesta += f"   • Total: ${ventas_mes['total_ventas']:,.2f}\n"
        respuesta += f"   • Transacciones: {ventas_mes['total_transacciones']}\n"
        respuesta += f"   • Clientes únicos: {ventas_mes['clientes_unicos']}\n\n"
        
        # Comparativa
        if comparativa['tendencia'] == 'crecimiento':
            emoji = '📈'
        elif comparativa['tendencia'] == 'decrecimiento':
            emoji = '📉'
        else:
            emoji = '➡️'
        
        respuesta += f"{emoji} **Comparativa Mensual:**\n"
        respuesta += f"   • Mes actual: ${comparativa['ventas_mes_actual']:,.2f}\n"
        respuesta += f"   • Mes anterior: ${comparativa['ventas_mes_anterior']:,.2f}\n"
        respuesta += f"   • Cambio: {comparativa['porcentaje_cambio']:+.2f}%\n"
        respuesta += f"   • Tendencia: {comparativa['tendencia'].upper()}\n"
        
        return respuesta
    
    def responder_productos(self) -> str:
        """Muestra información de productos e inventario"""
        cantidad = self.db.obtener_cantidad_productos()
        bajo_inventario = self.db.obtener_alerta_bajo_inventario()
        
        respuesta = "📦 **INFORMACIÓN DE INVENTARIO**\n\n"
        respuesta += f"**Total de productos:** {cantidad}\n\n"
        
        if not bajo_inventario.empty:
            respuesta += f"🚨 **ALERTAS DE BAJO INVENTARIO:** {len(bajo_inventario)} productos\n\n"
            
            respuesta += "**Top 5 productos con menos stock:**\n"
            for idx, row in bajo_inventario.head(5).iterrows():
                respuesta += f"• **{row['producto']}** ({row['categoria']})\n"
                respuesta += f"  Stock actual: {int(row['stock_actual'])} | "
                respuesta += f"Mínimo: {int(row['stock_minimo'])}\n"
                respuesta += f"  Faltan: {int(row['unidades_faltantes'])} unidades\n"
                respuesta += f"  Costo reposición: ${row['costo_reposicion']:,.2f}\n\n"
            
            costo_total = bajo_inventario['costo_reposicion'].sum()
            respuesta += f"💵 **Costo total de reposición:** ${costo_total:,.2f}\n"
        else:
            respuesta += "✅ No hay alertas de bajo inventario.\n"
        
        return respuesta
    
    def responder_alertas(self) -> str:
        """Muestra alertas de productos"""
        productos_vencer = self.db.obtener_productos_proximos_vencer(30)
        bajo_inventario = self.db.obtener_alerta_bajo_inventario()
        
        respuesta = "⚠️  **ALERTAS DEL SISTEMA**\n\n"
        
        # Productos próximos a vencer
        if not productos_vencer.empty:
            respuesta += f"📅 **PRODUCTOS PRÓXIMOS A VENCER:** {len(productos_vencer)}\n\n"
            
            # Críticos (menos de 7 días)
            criticos = productos_vencer[productos_vencer['dias_hasta_vencer'] <= 7]
            if not criticos.empty:
                respuesta += "🔴 **CRÍTICOS (≤ 7 días):**\n"
                for idx, row in criticos.iterrows():
                    respuesta += f"• {row['producto']} - {int(row['dias_hasta_vencer'])} días\n"
                    respuesta += f"  Stock: {int(row['stock_actual'])} | "
                    respuesta += f"Valor: ${row['valor_inventario']:,.2f}\n"
                respuesta += "\n"
            
            # Advertencias (7-30 días)
            advertencias = productos_vencer[productos_vencer['dias_hasta_vencer'] > 7]
            if not advertencias.empty:
                respuesta += f"🟡 **ADVERTENCIA (8-30 días):** {len(advertencias)} productos\n\n"
        else:
            respuesta += "✅ No hay productos próximos a vencer.\n\n"
        
        # Bajo inventario
        if not bajo_inventario.empty:
            respuesta += f"🚨 **BAJO INVENTARIO:** {len(bajo_inventario)} productos\n"
            respuesta += f"💵 Costo reposición: ${bajo_inventario['costo_reposicion'].sum():,.2f}\n"
        else:
            respuesta += "✅ No hay alertas de bajo inventario.\n"
        
        return respuesta
    
    # =========================================================================
    # RESPUESTAS VETERINARIAS (FALLBACK)
    # =========================================================================
    
    def responder_sintomas_enfermedad(self) -> str:
        """Responde a consultas sobre síntomas y enfermedades"""
        return """
🏥 **CONSULTA VETERINARIA**

⚠️ **IMPORTANTE:** Los síntomas que describes requieren atención veterinaria profesional.

📋 **Recomendaciones inmediatas:**

1. **Evalúa la gravedad:**
   • Fiebre > 39.5°C → Urgente
   • Hinchazón rápida → Urgente
   • Sangrado → Urgente
   • Dificultad para respirar → Emergencia

2. **Mientras tanto:**
   • Mantén a tu mascota cómoda y tranquila
   • Proporciona agua fresca
   • No auto-mediques
   • Observa otros síntomas

3. **Consulta veterinaria:**
   📞 Llama o agenda una cita
   🏥 Si es urgente, acude inmediatamente
   📝 Anota todos los síntomas y cuándo comenzaron

💡 **Para síntomas específicos:**
• Fiebre + hinchazón de oreja → Puede ser infección de oído
• Vómitos persistentes → Posible intoxicación o gastritis
• Diarrea → Parasitosis o cambio de alimentación
• Tos → Infección respiratoria

📞 **¿Necesitas agendar una cita?** 
Puedo ayudarte a buscar información en el sistema.
"""
    
    def responder_consulta_veterinaria(self) -> str:
        """Responde a consultas veterinarias generales"""
        return """
🩺 **CONSULTA VETERINARIA**

Entiendo tu preocupación por tu mascota. Para brindarte la mejor atención:

📋 **Información que necesito:**
• Tipo de mascota (perro, gato, etc.)
• Edad aproximada
• Síntomas específicos
• Cuándo comenzaron los síntomas
• ¿Ha comido algo inusual?

⚠️ **SEÑALES DE ALERTA - Acude inmediatamente si:**
• Dificultad para respirar
• Sangrado abundante
• Convulsiones
• Pérdida de conciencia
• Abdomen hinchado y duro
• Llanto constante de dolor

✅ **Puedo ayudarte con:**
• Agendar una cita
• Revisar historial médico
• Información sobre vacunas
• Cuidados preventivos

📞 Para emergencias, contacta directamente a tu veterinario de confianza.
"""
    
    def responder_vacunas(self) -> str:
        """Responde sobre vacunas"""
        return """
💉 **INFORMACIÓN SOBRE VACUNAS**

🐕 **PERROS - Vacunas esenciales:**

**Cachorros (6-16 semanas):**
• 6-8 sem: Primera vacuna múltiple
• 10-12 sem: Segunda dosis
• 14-16 sem: Tercera dosis + Rabia

**Adultos (Anual):**
• Refuerzo múltiple
• Rabia (cada 1-3 años según vacuna)
• Tos de las perreras (opcional)

🐱 **GATOS - Vacunas esenciales:**

**Gatitos (6-16 semanas):**
• 6-8 sem: Primera triple felina
• 10-12 sem: Segunda dosis
• 14-16 sem: Tercera dosis + Rabia

**Adultos (Anual):**
• Refuerzo triple felina
• Rabia
• Leucemia (si tiene acceso al exterior)

💡 **Importante:**
• Lleva registro de vacunas
• Respeta las fechas de refuerzo
• Consulta si hay reacción adversa

📞 **¿Quieres agendar vacunación?**
Puedo ayudarte a verificar el historial y programar citas.
"""
    
    def responder_desparasitacion(self) -> str:
        """Responde sobre desparasitación"""
        return """
🐛 **DESPARASITACIÓN**

📅 **Calendario recomendado:**

**Cachorros/Gatitos:**
• 2, 4, 6, 8 semanas de edad
• Luego mensual hasta los 6 meses
• Después cada 3-6 meses

**Adultos:**
• Cada 3-6 meses
• Cada 3 meses si tiene acceso al exterior

🔍 **Señales de parásitos:**
• Diarrea o vómito
• Abdomen hinchado
• Pérdida de peso
• Picazón anal (se arrastra)
• Gusanos visibles en heces
• Pulgas o garrapatas

💊 **Tipos de desparasitantes:**
• Internos (pastillas/jarabes)
• Externos (pipetas/collares)
• Combinados

⚠️ **Importante:**
• Usa productos recomendados por veterinario
• Dosis según peso
• Desparasita a todas las mascotas de la casa

📞 ¿Necesitas consultar el historial de desparasitación de tu mascota?
"""
    
    def responder_alimentacion(self) -> str:
        """Responde sobre alimentación"""
        return """
🍽️ **ALIMENTACIÓN PARA MASCOTAS**

🐕 **PERROS:**

**Cachorros (hasta 12 meses):**
• Alimento especial para cachorros
• 3-4 comidas al día
• Rico en proteínas y calcio

**Adultos:**
• 2 comidas al día
• Alimento balanceado de calidad
• Controlar porciones

**Mayores (>7 años):**
• Alimento senior
• Menor grasa, más fibra
• Suplementos articulares

🐱 **GATOS:**

**Gatitos (hasta 12 meses):**
• Alimento para gatitos
• 3-4 comidas pequeñas
• Alto en proteínas

**Adultos:**
• 2-3 comidas al día
• Alimento balanceado
• Mucha agua fresca

❌ **NUNCA les des:**
• Chocolate
• Cebolla/Ajo
• Uvas/Pasas
• Aguacate
• Huesos cocidos
• Dulces/Cafeína

💡 **Consejos:**
• Transición gradual al cambiar alimento (7-10 días)
• Agua fresca siempre disponible
• Controla el peso regularmente

📞 ¿Necesitas recomendación específica? Consulta con tu veterinario.
"""
    
    def responder_cuidados(self) -> str:
        """Responde sobre cuidados generales"""
        return """
🐾 **CUIDADOS GENERALES**

🛁 **HIGIENE:**

**Baño:**
• Perros: Cada 4-8 semanas
• Gatos: Según necesidad (se limpian solos)
• Usa shampoo específico para mascotas

**Cepillado:**
• Diario para pelo largo
• 2-3 veces/semana para pelo corto
• Reduce bolas de pelo en gatos

**Uñas:**
• Corte cada 4-6 semanas
• Cuidado con la vena (parte rosada)

**Dientes:**
• Cepillado diario ideal
• Snacks dentales
• Limpieza profesional anual

🏃 **EJERCICIO:**

**Perros:**
• 30-120 min diarios según raza
• Paseos y juegos
• Socialización

**Gatos:**
• 10-15 min de juego activo
• Rascadores
• Juguetes interactivos

🏥 **SALUD PREVENTIVA:**
• Visitas veterinarias: 1-2 al año
• Vacunas al día
• Desparasitación regular
• Control de peso

💚 **BIENESTAR EMOCIONAL:**
• Ambiente enriquecido
• Rutinas consistentes
• Atención y cariño
• Espacio propio

📞 ¿Necesitas más información sobre algún cuidado específico?
"""
    
    def responder_emergencia(self) -> str:
        """Responde a situaciones de emergencia"""
        return """
🚨 **EMERGENCIA VETERINARIA**

⚠️ **ACTÚA RÁPIDO - Lleva a tu mascota al veterinario INMEDIATAMENTE si:**

🔴 **EMERGENCIAS CRÍTICAS:**
• Dificultad para respirar
• Sangrado que no para
• Convulsiones
• Pérdida de conciencia
• Trauma severo (atropellamiento, caída)
• Abdomen hinchado y duro
• Intoxicación conocida
• Fiebre > 40°C
• Ojos: dolor súbito o pérdida de visión

🟠 **URGENCIAS (No esperes más de 2-4 horas):**
• Vómitos persistentes
• Diarrea con sangre
• No come ni bebe por 24h
• Dolor evidente
• Dificultad para orinar
• Hinchazón rápida

📞 **MIENTRAS LLEGAS AL VETERINARIO:**

1. **Mantén la calma** - Tu mascota siente tu nerviosismo
2. **Transporte seguro** - Caja transportadora o manta
3. **No des medicamentos** - Espera instrucciones del vet
4. **Llama antes** - Avisa que vas en camino
5. **Lleva historial** - Si tienes cartilla de vacunación

💡 **NÚMEROS DE EMERGENCIA:**
• Guarda el número de tu veterinario
• Ten a mano clínicas 24h cercanas
• Centro de toxicología veterinaria

⏱️ **En emergencias, CADA MINUTO CUENTA**

¿Necesito ayuda para encontrar veterinarios de emergencia cercanos?
"""
    
    def responder_clustering(self) -> str:
        """Responde sobre análisis de clustering"""
        try:
            df = self.db.obtener_dataset_completo()
            
            if df.empty:
                return "❌ No hay datos suficientes para realizar clustering."
            
            # Realizar análisis de clustering
            analisis = self.predictor.analisis_clustering_completo(df)
            
            respuesta = "🔬 **ANÁLISIS DE HIERARCHICAL CLUSTERING**\n\n"
            respuesta += "Agrupamiento jerárquico de datos usando IA\n\n"
            
            # Clustering de Mascotas
            if "clustering_mascotas" in analisis and "error" not in analisis['clustering_mascotas']:
                cm = analisis['clustering_mascotas']
                respuesta += f"🐾 **CLUSTERS DE MASCOTAS:** {cm['n_clusters']} grupos\n"
                respuesta += f"   Calidad (Silhouette): {cm['silhouette_score']:.3f}\n\n"
                
                for cluster in cm['clusters'][:3]:
                    respuesta += f"   **Cluster {cluster['cluster_id']}:**\n"
                    respuesta += f"   • Total: {cluster['total_mascotas']} mascotas\n"
                    respuesta += f"   • Edad promedio: {cluster['edad_promedio']:.1f} años\n"
                    respuesta += f"   • Tipo predominante: {cluster['tipo_mascota_predominante']}\n\n"
            
            # Clustering de Clientes
            if "clustering_clientes" in analisis and "error" not in analisis['clustering_clientes']:
                cc = analisis['clustering_clientes']
                respuesta += f"👥 **SEGMENTACIÓN DE CLIENTES:** {cc['n_segmentos']} segmentos\n"
                respuesta += f"   Calidad: {cc['calidad_clustering']}\n\n"
                
                for segmento in cc['segmentos'][:3]:
                    respuesta += f"   **{segmento['nombre']}:**\n"
                    respuesta += f"   • Clientes: {segmento['total_clientes']}\n"
                    respuesta += f"   • Gasto promedio: ${segmento['gasto_promedio']:.2f}\n"
                    respuesta += f"   • Citas promedio: {segmento['citas_promedio']:.1f}\n\n"
            
            # Clustering de Servicios
            if "clustering_servicios" in analisis and "error" not in analisis['clustering_servicios']:
                cs = analisis['clustering_servicios']
                respuesta += f"🏥 **GRUPOS DE SERVICIOS:** {cs['n_grupos']}\n\n"
                
                for grupo in cs['grupos'][:3]:
                    respuesta += f"   **Grupo {grupo['grupo_id']}:** {grupo['total_servicios']} servicios\n"
                    respuesta += f"   • Hora promedio: {grupo['hora_promedio']:.1f}:00\n"
                    servicios_txt = ", ".join(grupo['servicios'][:3])
                    if len(grupo['servicios']) > 3:
                        servicios_txt += f" y {len(grupo['servicios'])-3} más"
                    respuesta += f"   • Servicios: {servicios_txt}\n\n"
            
            respuesta += "\n💡 **Método:** Agglomerative Hierarchical Clustering\n"
            respuesta += "📊 Este análisis identifica patrones ocultos en tus datos."
            
            return respuesta
            
        except Exception as e:
            logger.error(f"Error en clustering: {e}")
            return f"❌ Error al generar clustering: {str(e)}"
    
    # =========================================================================
    # PROCESAMIENTO PRINCIPAL
    # =========================================================================
    
    def procesar_mensaje(self, mensaje: str) -> Dict:
        """
        Procesa un mensaje del usuario y genera respuesta
        
        Proceso:
        1. Usa la red neuronal para detectar la intención
        2. Si es una intención veterinaria, responde con información médica
        3. Si es una consulta de datos, consulta la base de datos
        4. Si no entiende, da respuesta genérica
        
        Returns:
            Dict con respuesta, intención, confianza y timestamp
        """
        # Usar red neuronal para detectar intención
        intencion, confianza = self.predecir_intencion_neuronal(mensaje)
        
        # Obtener respuesta según la intención
        if intencion == "desconocido" or self.chatbot_model is None:
            # Fallback: usar detección de patrones simple
            intencion = self.detectar_intencion(mensaje)
            confianza = 0.5
        
        # Generar respuesta según intención
        
        # Respuestas de la red neuronal veterinaria (intenciones médicas)
        if intencion in self.intents:
            # Obtener respuesta aleatoria de las disponibles para esta intención
            respuestas_disponibles = self.intents[intencion]
            respuesta = random.choice(respuestas_disponibles)
        
        # Respuestas que requieren consulta a base de datos
        elif intencion == 'estadisticas_db' or intencion == 'estadisticas':
            respuesta = self.responder_estadisticas()
            
        elif intencion == 'tipo_mascota_comun' or intencion == 'tipo_mas_comun':
            respuesta = self.responder_tipo_mas_comun()
            
        elif intencion == 'dia_mas_atencion':
            respuesta = self.responder_dia_mas_atencion()
        
        # Fallback para intenciones antiguas (compatibilidad)
        elif intencion == 'ayuda':
            respuesta = self.responder_ayuda()
            
        elif intencion == 'servicios':
            respuesta = self.responder_servicios()
            
        elif intencion == 'buscar_mascota':
            # Extraer nombre
            palabras = mensaje.lower().split()
            if 'mascota' in palabras:
                idx = palabras.index('mascota') + 1
                nombre = ' '.join(palabras[idx:]) if idx < len(palabras) else ''
            else:
                nombre = ''
            respuesta = self.responder_buscar_mascota(nombre)
            
        elif intencion == 'prediccion':
            respuesta = self.responder_prediccion_tipo()
        
        elif intencion == 'entrenar':
            respuesta = """
🎓 **ENTRENAR MODELOS DE IA**

⚠️ **Nota:** El entrenamiento de modelos NO se puede hacer desde el chat.

📋 **Cómo entrenar:**

1️⃣ **Desde terminal:**
   ```
   python entrenar_chatbot_veterinario.py
   ```
   
2️⃣ **O desde la API (segundo plano):**
   ```
   POST http://localhost:8000/api/entrenar
   ```

⏱️ **Tiempo estimado:** 5-10 minutos

📊 **¿Qué hace el entrenamiento?**
• Entrena red neuronal con datos de citas
• Mejora predicciones de tipos de mascota
• Aumenta precisión de asistencia a citas

✅ **Estado actual:**
• Modelos entrenados: """ + ("Sí ✅" if self.predictor.trained else "No ❌") + """
• Sistema funcional: Sí (usando análisis de datos)

💡 **Tip:** Si los modelos no están entrenados, el sistema sigue funcionando perfectamente usando consultas directas a la base de datos.
"""
        
        # Nuevas intenciones de negocio
        elif intencion == 'citas_hoy':
            respuesta = self.responder_citas_hoy()
            
        elif intencion == 'ventas':
            respuesta = self.responder_ventas()
            
        elif intencion == 'productos':
            respuesta = self.responder_productos()
            
        elif intencion == 'alertas':
            respuesta = self.responder_alertas()
        
        # Intenciones veterinarias (fallback si modelo no está entrenado)
        elif intencion == 'sintomas_enfermedad':
            respuesta = self.responder_sintomas_enfermedad()
            
        elif intencion == 'consulta_veterinaria':
            respuesta = self.responder_consulta_veterinaria()
            
        elif intencion == 'vacunas':
            respuesta = self.responder_vacunas()
            
        elif intencion == 'desparasitacion':
            respuesta = self.responder_desparasitacion()
            
        elif intencion == 'alimentacion':
            respuesta = self.responder_alimentacion()
            
        elif intencion == 'cuidados':
            respuesta = self.responder_cuidados()
            
        elif intencion == 'emergencia':
            respuesta = self.responder_emergencia()
        
        elif intencion == 'clustering':
            respuesta = self.responder_clustering()
            
        else:
            respuesta = """
❓ No entendí tu pregunta. 

Puedo ayudarte con:

🏥 **INFORMACIÓN VETERINARIA:**
• Síntomas y enfermedades
• Vacunas y desparasitación
• Emergencias veterinarias

💼 **MÉTRICAS DE NEGOCIO:**
• Citas del día
• Ventas del mes
• Alertas de inventario

📊 **ANÁLISIS Y DATOS:**
• Estadísticas del sistema
• Tipo de mascota más común
• Predicciones con IA

💬 **Ejemplos:**
• "Mi gata tiene fiebre"
• "¿Qué vacunas necesita un cachorro?"
• "¿Cuántas citas hay hoy?"

✍️ Escribe tu pregunta y te ayudaré.
"""
            confianza = 0.3
        
        return {
            "respuesta": respuesta,
            "intencion": intencion,
            "confianza": confianza,
            "timestamp": datetime.now().isoformat()
        }
    
    # =========================================================================
    # MODO INTERACTIVO
    # =========================================================================
    
    def iniciar_chat_interactivo(self):
        """Inicia un chat interactivo en consola"""
        print("=" * 80)
        print(f"🤖 {self.nombre_bot} - Asistente Virtual Pet Store")
        print("=" * 80)
        print("\n¡Hola! Soy tu asistente virtual. Escribe 'ayuda' para ver qué puedo hacer.")
        print("Escribe 'salir' para terminar la conversación.\n")
        
        while True:
            try:
                # Leer entrada del usuario
                mensaje = input("👤 Tú: ").strip()
                
                if not mensaje:
                    continue
                
                # Salir si el usuario lo solicita
                if mensaje.lower() in ['salir', 'exit', 'quit']:
                    print(f"\n🤖 {self.nombre_bot}: ¡Hasta pronto! 👋\n")
                    break
                
                # Comando especial: entrenar modelos
                if mensaje.lower() == 'entrenar':
                    print(f"\n🤖 {self.nombre_bot}: Entrenando modelos...")
                    self.entrenar_modelos()
                    continue
                
                # Procesar mensaje
                resultado = self.procesar_mensaje(mensaje)
                
                # Mostrar respuesta
                print(f"\n🤖 {self.nombre_bot}:")
                print(resultado['respuesta'])
                print(f"\n   [Confianza: {resultado['confianza']:.0%}]\n")
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 {self.nombre_bot}: ¡Hasta pronto! 👋\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def entrenar_modelos(self):
        """Entrena los modelos de red neuronal"""
        print("\n🚀 Iniciando entrenamiento de modelos...")
        print("⏱️  Esto puede tardar varios minutos...\n")
        
        try:
            # Obtener datos
            df = self.db.obtener_dataset_completo()
            
            if df.empty:
                print("❌ No hay datos suficientes para entrenar.\n")
                return
            
            print(f"📊 Dataset cargado: {len(df)} registros\n")
            
            # Entrenar modelos
            self.predictor.entrenar_modelo_tipo_mascota(df)
            self.predictor.entrenar_modelo_asistencia(df)
            
            # Guardar modelos
            self.predictor.guardar_modelos()
            
            print("\n✅ ¡Modelos entrenados y guardados exitosamente!\n")
            
        except Exception as e:
            print(f"\n❌ Error durante el entrenamiento: {e}\n")
    
    def cerrar(self):
        """Cierra conexiones"""
        self.db.cerrar()


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    try:
        bot = PetStoreBot()
        bot.iniciar_chat_interactivo()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Adiós!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

