"""
SCRIPT DE ENTRENAMIENTO PARA TRANSFORMER CHATBOT
Entrena el modelo Transformer con datos de conversaciones y contexto del negocio
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import os
import numpy as np
from typing import List, Tuple
from tqdm import tqdm
import logging

from transformer_chatbot import TransformerChatbot, PetStoreBotTransformer
from config_transformer import get_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# DATASET PARA ENTRENAMIENTO
# =============================================================================

class ChatDataset(Dataset):
    """
    Dataset para entrenar el transformer
    Contiene pares (pregunta, respuesta) del chatbot
    """
    
    def __init__(self, data_pairs: List[Tuple[str, str]], bot: PetStoreBotTransformer, max_len: int = 128):
        self.data_pairs = data_pairs
        self.bot = bot
        self.max_len = max_len
    
    def __len__(self):
        return len(self.data_pairs)
    
    def __getitem__(self, idx):
        pregunta, respuesta = self.data_pairs[idx]
        
        # Convertir a tensores
        input_tensor = self.bot.texto_a_indices(pregunta, self.max_len)
        target_tensor = self.bot.texto_a_indices(respuesta, self.max_len)
        
        return input_tensor, target_tensor


# =============================================================================
# DATOS DE ENTRENAMIENTO
# =============================================================================

def generar_datos_entrenamiento():
    """
    Genera datos de entrenamiento para el chatbot
    Combina ejemplos predefinidos con consultas del dominio Pet Store
    """
    
    training_data = [
        # Saludos y conversación básica
        ("hola", "¡Hola! 👋 Soy tu asistente virtual del Pet Store. ¿En qué puedo ayudarte?"),
        ("buenos dias", "¡Buenos días! Estoy aquí para ayudarte con información sobre mascotas y servicios."),
        ("como estas", "¡Muy bien! Listo para ayudarte. ¿Qué necesitas saber?"),
        ("adios", "¡Hasta pronto! 👋 Cuida bien a tus mascotas 🐾"),
        ("gracias", "¡De nada! Estoy aquí para ayudarte. 😊"),
        
        # Estadísticas
        ("muestrame las estadisticas", "Te muestro las estadísticas generales del sistema con información actualizada."),
        ("cuantas mascotas hay", "Déjame consultar el número total de mascotas registradas en el sistema."),
        ("cuantos clientes tenemos", "Voy a revisar el total de clientes registrados en la base de datos."),
        ("dame un reporte", "Por supuesto, preparo un reporte completo con las métricas principales."),
        ("metricas del negocio", "Aquí están las métricas clave del negocio con datos en tiempo real."),
        
        # Citas
        ("cuantas citas hay hoy", "Déjame consultar las citas programadas para el día de hoy."),
        ("hay citas programadas", "Voy a revisar la agenda de citas para informarte."),
        ("proximas citas", "Te muestro las próximas citas programadas en el sistema."),
        ("agenda del dia", "Aquí está la agenda completa del día con todas las citas."),
        
        # Ventas
        ("cuanto vendimos hoy", "Voy a consultar el total de ventas realizadas hoy."),
        ("ventas del mes", "Te muestro el reporte de ventas del mes actual con detalles."),
        ("cuales son los ingresos", "Aquí está el análisis de ingresos con información detallada."),
        ("transacciones del dia", "Déjame revisar las transacciones realizadas el día de hoy."),
        
        # Mascotas
        ("tipo de mascota mas comun", "Voy a analizar qué tipo de mascota es el más común en nuestro sistema."),
        ("que mascotas tenemos", "Te muestro la distribución de tipos de mascotas registradas."),
        ("razas mas frecuentes", "Aquí está el análisis de las razas más frecuentes."),
        
        # Productos e Inventario
        ("cuantos productos tenemos", "Déjame consultar la cantidad total de productos en inventario."),
        ("productos proximos a vencer", "Voy a revisar los productos que están próximos a su fecha de vencimiento."),
        ("alertas de inventario", "Te muestro las alertas de productos con bajo stock."),
        ("stock bajo", "Aquí están los productos que necesitan reposición urgente."),
        
        # Predicciones
        ("predice tipo de mascota", "Voy a usar el modelo de machine learning para hacer una predicción."),
        ("que predicciones tienes", "Puedo hacer predicciones sobre tipos de mascotas y asistencia a citas."),
        
        # Clustering
        ("analisis de clustering", "Voy a ejecutar el análisis de clustering jerárquico sobre los datos."),
        ("segmenta clientes", "Te muestro la segmentación de clientes usando machine learning."),
        ("agrupa mascotas", "Aquí está el agrupamiento de mascotas por características similares."),
        
        # Ayuda
        ("que puedes hacer", "Puedo ayudarte con estadísticas, citas, ventas, inventario y predicciones con IA."),
        ("ayuda", "Estoy aquí para ayudarte con información del negocio y análisis inteligentes."),
        ("comandos disponibles", "Puedo procesar consultas sobre métricas, citas, ventas, productos y más."),
        
        # Contexto específico Pet Store
        ("servicios disponibles", "Te muestro la lista completa de servicios veterinarios disponibles."),
        ("horario de atencion", "Déjame consultar los horarios y disponibilidad de atención."),
        ("veterinarios", "Aquí está la información sobre los veterinarios del equipo."),
        
        # Consultas complejas
        ("dame un resumen completo", "Te preparo un resumen ejecutivo con todas las métricas principales."),
        ("como va el negocio", "Te muestro un análisis completo del estado actual del negocio."),
        ("que necesita atencion", "Aquí están los puntos que requieren atención inmediata."),
        
        # Análisis de tendencias
        ("cual es la tendencia", "Voy a analizar las tendencias en ventas y atención a clientes."),
        ("comparativa con mes anterior", "Te muestro la comparativa de ventas con el mes anterior."),
        ("estamos creciendo", "Aquí está el análisis de crecimiento del negocio."),
    ]
    
    return training_data


def guardar_datos_entrenamiento(filename='data/chatbot_training_data.json'):
    """
    Guarda los datos de entrenamiento en un archivo JSON
    """
    datos = generar_datos_entrenamiento()
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Datos de entrenamiento guardados en {filename}")
    logger.info(f"   Total de ejemplos: {len(datos)}")


def cargar_datos_entrenamiento(filename='data/chatbot_training_data.json'):
    """
    Carga los datos de entrenamiento desde un archivo JSON
    """
    if not os.path.exists(filename):
        logger.warning(f"Archivo {filename} no encontrado, generando datos...")
        guardar_datos_entrenamiento(filename)
    
    with open(filename, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    logger.info(f"✅ Datos de entrenamiento cargados: {len(datos)} ejemplos")
    return datos


# =============================================================================
# FUNCIÓN DE ENTRENAMIENTO
# =============================================================================

def entrenar_transformer(
    epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.0001,
    device: str = None
):
    """
    Entrena el modelo Transformer del chatbot
    
    Args:
        epochs: Número de épocas de entrenamiento
        batch_size: Tamaño del batch
        learning_rate: Tasa de aprendizaje
        device: Dispositivo (cuda/cpu)
    """
    
    # Determinar dispositivo
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"🔧 Usando dispositivo: {device}")
    
    # Inicializar bot
    logger.info("🤖 Inicializando chatbot...")
    bot = PetStoreBotTransformer()
    
    # Cargar datos de entrenamiento
    logger.info("📚 Cargando datos de entrenamiento...")
    datos = cargar_datos_entrenamiento()
    
    # Construir vocabulario
    logger.info("📝 Construyendo vocabulario...")
    textos = []
    for pregunta, respuesta in datos:
        textos.append(pregunta)
        textos.append(respuesta)
    bot.construir_vocabulario(textos)
    
    # Crear modelo
    logger.info("🏗️  Creando modelo Transformer...")
    bot.model = TransformerChatbot(
        vocab_size=bot.vocab_size,
        d_model=bot.d_model,
        num_heads=bot.num_heads,
        num_layers=bot.num_layers,
        d_ff=bot.d_ff,
        max_len=bot.max_len,
        dropout=bot.dropout
    ).to(device)
    
    # Crear dataset y dataloader
    dataset = ChatDataset(datos, bot, bot.max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Configurar optimizador y función de pérdida
    optimizer = optim.Adam(bot.model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=bot.word2idx[bot.PAD_TOKEN])
    
    logger.info(f"\n{'='*80}")
    logger.info(f"🚀 INICIANDO ENTRENAMIENTO")
    logger.info(f"{'='*80}")
    logger.info(f"Épocas: {epochs}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Learning rate: {learning_rate}")
    logger.info(f"Vocabulario: {bot.vocab_size} palabras")
    logger.info(f"Parámetros del modelo: {sum(p.numel() for p in bot.model.parameters()):,}")
    logger.info(f"{'='*80}\n")
    
    # Entrenamiento
    bot.model.train()
    for epoch in range(epochs):
        total_loss = 0
        progress_bar = tqdm(dataloader, desc=f"Época {epoch+1}/{epochs}")
        
        for batch_idx, (inputs, targets) in enumerate(progress_bar):
            inputs = inputs.to(device)
            targets = targets.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = bot.model(inputs)
            
            # Calcular pérdida
            loss = criterion(outputs.view(-1, bot.vocab_size), targets.view(-1))
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(bot.model.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
            progress_bar.set_postfix({'loss': loss.item()})
        
        avg_loss = total_loss / len(dataloader)
        logger.info(f"Época {epoch+1}/{epochs} - Pérdida promedio: {avg_loss:.4f}")
        
        # Guardar checkpoint cada 10 épocas
        if (epoch + 1) % 10 == 0:
            bot.guardar_modelo()
            logger.info(f"💾 Checkpoint guardado en época {epoch+1}")
    
    # Guardar modelo final
    logger.info("\n💾 Guardando modelo final...")
    bot.model_trained = True
    bot.guardar_modelo()
    
    logger.info(f"\n{'='*80}")
    logger.info("✅ ENTRENAMIENTO COMPLETADO")
    logger.info(f"{'='*80}\n")
    
    # Probar el modelo
    logger.info("🧪 Probando el modelo entrenado...\n")
    probar_modelo(bot)
    
    return bot


def probar_modelo(bot: PetStoreBotTransformer):
    """
    Prueba el modelo entrenado con ejemplos
    """
    ejemplos = [
        "hola",
        "muéstrame las estadísticas",
        "cuántas citas hay hoy",
        "dame el reporte de ventas"
    ]
    
    for ejemplo in ejemplos:
        print(f"\n👤 Usuario: {ejemplo}")
        resultado = bot.procesar_mensaje(ejemplo)
        print(f"🤖 Bot ({resultado['modelo']}): {resultado['respuesta']}")
        print(f"   Confianza: {resultado['confianza']:.0%}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎓 ENTRENAMIENTO DEL CHATBOT TRANSFORMER")
    print("="*80 + "\n")
    
    # Configuración
    config = get_config('TRANSFORMER_CONFIG')
    
    # Generar y guardar datos de entrenamiento
    logger.info("Preparando datos de entrenamiento...")
    guardar_datos_entrenamiento()
    
    # Entrenar modelo
    try:
        bot = entrenar_transformer(
            epochs=config['num_epochs'],
            batch_size=config['batch_size'],
            learning_rate=config['learning_rate']
        )
        
        print("\n✅ ¡Modelo entrenado exitosamente!")
        print("\n💡 Para usar el modelo, ejecuta:")
        print("   python api.py")
        print("\nO pruébalo directamente:")
        print("   python transformer_chatbot.py")
        
    except Exception as e:
        logger.error(f"\n❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80 + "\n")

