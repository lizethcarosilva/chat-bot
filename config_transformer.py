"""
CONFIGURACIÓN DEL CHATBOT TRANSFORMER
Parámetros y configuraciones para el modelo Transformer
"""

# =============================================================================
# CONFIGURACIÓN DEL MODELO TRANSFORMER
# =============================================================================

TRANSFORMER_CONFIG = {
    # Dimensiones del modelo
    'd_model': 256,          # Dimensión de embeddings y hidden states
    'num_heads': 8,          # Número de attention heads
    'num_layers': 4,         # Número de bloques transformer
    'd_ff': 1024,            # Dimensión de la capa feed-forward
    'max_len': 128,          # Longitud máxima de secuencia
    'dropout': 0.1,          # Tasa de dropout
    
    # Vocabulario
    'vocab_size': 5000,      # Tamaño máximo del vocabulario
    'min_word_freq': 2,      # Frecuencia mínima para incluir palabra
    
    # Tokens especiales
    'PAD_TOKEN': '<PAD>',    # Padding
    'SOS_TOKEN': '<SOS>',    # Start of sequence
    'EOS_TOKEN': '<EOS>',    # End of sequence
    'UNK_TOKEN': '<UNK>',    # Unknown word
    
    # Generación de texto
    'temperature': 0.8,      # Controla aleatoriedad (0.1-1.5)
    'top_k': 50,             # Top-K sampling
    'top_p': 0.9,            # Nucleus sampling
    'max_generate_length': 100,  # Longitud máxima de respuesta generada
    'beam_size': 3,          # Tamaño del beam para beam search
    
    # Entrenamiento
    'batch_size': 32,
    'learning_rate': 0.0001,
    'num_epochs': 50,
    'warmup_steps': 4000,
    'gradient_clip': 1.0,
    
    # Rutas de archivos
    'model_path': 'models/transformer_chatbot.pth',
    'vocab_path': 'models/transformer_vocab.pkl',
    'training_data': 'data/chatbot_training_data.json',
}

# =============================================================================
# CONFIGURACIÓN DE INTENCIONES Y RESPUESTAS BASE
# =============================================================================

INTENCIONES_BASE = {
    'saludo': [
        '¡Hola! 👋 Soy tu asistente virtual con IA Transformer. ¿En qué puedo ayudarte?',
        '¡Bienvenido! Estoy aquí para asistirte con información del Pet Store.',
        '¡Hola! Puedo ayudarte con estadísticas, citas, ventas y más.'
    ],
    'despedida': [
        '¡Hasta pronto! 👋 Cuida bien a tus mascotas 🐾',
        '¡Adiós! Regresa cuando necesites ayuda.',
        '¡Nos vemos! Que tengas un excelente día.'
    ],
    'agradecimiento': [
        '¡De nada! Estoy aquí para ayudarte. 😊',
        'Es un placer ayudarte. ¿Necesitas algo más?',
        'Para eso estoy aquí. ¿Algo más que pueda hacer por ti?'
    ]
}

# =============================================================================
# CONFIGURACIÓN DE CONTEXTO Y MEMORIA
# =============================================================================

CONTEXT_CONFIG = {
    'max_history': 5,           # Número máximo de mensajes en historial
    'context_window': 3,        # Ventana de contexto para generar respuesta
    'use_database_context': True,  # Enriquecer con datos de BD
    'confidence_threshold': 0.6,   # Umbral de confianza mínimo
}

# =============================================================================
# PALABRAS CLAVE PARA ENRIQUECIMIENTO CON BASE DE DATOS
# =============================================================================

DB_KEYWORDS = {
    'estadisticas': ['estadistica', 'estadisticas', 'metricas', 'reporte', 'resumen'],
    'citas': ['citas', 'cita', 'hoy', 'programadas', 'agenda'],
    'ventas': ['ventas', 'venta', 'vendido', 'ingresos', 'transacciones'],
    'productos': ['productos', 'producto', 'inventario', 'stock'],
    'mascotas': ['mascota', 'mascotas', 'tipo', 'raza', 'animal'],
    'clientes': ['cliente', 'clientes', 'propietario'],
    'alertas': ['alerta', 'alertas', 'vencimiento', 'vencer', 'bajo stock'],
}

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': 'logs/transformer_chatbot.log',
}

# =============================================================================
# CONFIGURACIÓN DE PYTORCH
# =============================================================================

PYTORCH_CONFIG = {
    'use_cuda': True,           # Usar GPU si está disponible
    'seed': 42,                 # Semilla para reproducibilidad
    'num_workers': 4,           # Workers para DataLoader
    'pin_memory': True,         # Optimización de memoria
}

# =============================================================================
# MENSAJES DEL SISTEMA
# =============================================================================

SYSTEM_MESSAGES = {
    'modelo_no_entrenado': """
🤖 **Sistema Híbrido Activo**

Actualmente estoy funcionando en modo híbrido, combinando:
- Detección de intenciones con patrones
- Respuestas enriquecidas con datos reales
- Análisis inteligente de consultas

Para activar el modelo Transformer completo, entrena el modelo ejecutando:
```python
python entrenar_transformer.py
```
    """,
    
    'error_generacion': """
⚠️ Hubo un problema generando la respuesta. 

Pero no te preocupes, puedo ayudarte con:
📊 Estadísticas del negocio
📅 Consultar citas
💰 Análisis de ventas
🐾 Información sobre mascotas

¿Qué necesitas?
    """,
    
    'bienvenida': """
🤖 **Chatbot con Transformer - Pet Store**

Tecnología:
✨ Arquitectura Transformer (Estado del arte en NLP)
🧠 Multi-Head Attention
📊 Enriquecimiento con datos en tiempo real
🎯 Generación contextual de respuestas

Capacidades:
• Consultas de estadísticas y métricas
• Análisis de ventas y citas
• Información sobre mascotas y clientes
• Predicciones con machine learning
• Alertas y reportes

¿En qué puedo ayudarte hoy?
    """
}

# =============================================================================
# CONFIGURACIÓN DE RESPUESTAS FALLBACK
# =============================================================================

FALLBACK_RESPONSES = [
    "No estoy seguro de entender. ¿Podrías reformular tu pregunta?",
    "Interesante pregunta. ¿Puedes darme más detalles?",
    "Hmm, no tengo suficiente información. ¿Puedes ser más específico?",
    "Déjame ayudarte mejor. ¿Qué información necesitas exactamente?",
]

# =============================================================================
# CONFIGURACIÓN DE PERFORMANCE
# =============================================================================

PERFORMANCE_CONFIG = {
    'cache_responses': True,      # Cachear respuestas frecuentes
    'cache_size': 100,            # Tamaño del caché
    'cache_ttl': 3600,            # Tiempo de vida del caché (segundos)
    'max_response_time': 3.0,     # Tiempo máximo de respuesta (segundos)
    'async_db_queries': True,     # Consultas asíncronas a BD
}

# =============================================================================
# CONFIGURACIÓN DE VALIDACIÓN
# =============================================================================

VALIDATION_CONFIG = {
    'max_input_length': 500,      # Longitud máxima de entrada
    'min_input_length': 1,        # Longitud mínima de entrada
    'filter_profanity': True,     # Filtrar lenguaje inapropiado
    'sanitize_input': True,       # Sanitizar entrada
}


# =============================================================================
# FUNCIÓN PARA OBTENER CONFIGURACIÓN
# =============================================================================

def get_config(config_name='TRANSFORMER_CONFIG'):
    """
    Obtiene la configuración especificada
    
    Args:
        config_name: Nombre de la configuración a obtener
    
    Returns:
        Diccionario con la configuración
    """
    configs = {
        'TRANSFORMER_CONFIG': TRANSFORMER_CONFIG,
        'INTENCIONES_BASE': INTENCIONES_BASE,
        'CONTEXT_CONFIG': CONTEXT_CONFIG,
        'DB_KEYWORDS': DB_KEYWORDS,
        'LOGGING_CONFIG': LOGGING_CONFIG,
        'PYTORCH_CONFIG': PYTORCH_CONFIG,
        'SYSTEM_MESSAGES': SYSTEM_MESSAGES,
        'FALLBACK_RESPONSES': FALLBACK_RESPONSES,
        'PERFORMANCE_CONFIG': PERFORMANCE_CONFIG,
        'VALIDATION_CONFIG': VALIDATION_CONFIG,
    }
    
    return configs.get(config_name, {})


def print_config():
    """Imprime la configuración actual"""
    print("=" * 80)
    print("CONFIGURACIÓN DEL CHATBOT TRANSFORMER")
    print("=" * 80)
    
    print("\n📊 MODELO:")
    for key, value in TRANSFORMER_CONFIG.items():
        if not key.endswith('_path'):
            print(f"  • {key}: {value}")
    
    print("\n🎯 CONTEXTO:")
    for key, value in CONTEXT_CONFIG.items():
        print(f"  • {key}: {value}")
    
    print("\n⚡ PERFORMANCE:")
    for key, value in PERFORMANCE_CONFIG.items():
        print(f"  • {key}: {value}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_config()

