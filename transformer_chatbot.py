"""
CHATBOT CON TRANSFORMER - GENERACIÓN DE RESPUESTAS CON RED NEURONAL TRANSFORMER
Utiliza arquitectura Transformer (similar a GPT) para generar respuestas contextuales
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging
import os
import pickle
from database import PetStoreDatabase
from predictor import PetStorePredictor

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# ARQUITECTURA TRANSFORMER
# =============================================================================

class MultiHeadAttention(nn.Module):
    """
    Mecanismo de Multi-Head Attention para Transformer
    """
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model debe ser divisible por num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Proyecciones lineales para Q, K, V
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        self.scale = torch.sqrt(torch.FloatTensor([self.d_k]))
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.shape[0]
        
        # Proyecciones lineales
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # Dividir en múltiples heads
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).permute(0, 2, 1, 3)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).permute(0, 2, 1, 3)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).permute(0, 2, 1, 3)
        
        # Calcular attention scores
        scores = torch.matmul(Q, K.permute(0, 1, 3, 2)) / self.scale.to(query.device)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Aplicar softmax
        attention = torch.softmax(scores, dim=-1)
        attention = self.dropout(attention)
        
        # Aplicar attention a valores
        x = torch.matmul(attention, V)
        
        # Concatenar heads
        x = x.permute(0, 2, 1, 3).contiguous()
        x = x.view(batch_size, -1, self.d_model)
        
        # Proyección final
        x = self.W_o(x)
        
        return x, attention


class PositionwiseFeedForward(nn.Module):
    """
    Feed-Forward Network para cada posición
    """
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.gelu = nn.GELU()
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.gelu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


class TransformerBlock(nn.Module):
    """
    Bloque Transformer completo (Attention + FFN + Normalization)
    """
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Multi-Head Attention con residual connection
        attn_output, _ = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed-Forward con residual connection
        ff_output = self.ff(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x


class PositionalEncoding(nn.Module):
    """
    Codificación posicional para Transformer
    """
    def __init__(self, d_model: int, max_len: int = 512, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        
        # Crear matriz de codificación posicional
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class TransformerChatbot(nn.Module):
    """
    Modelo Transformer completo para generación de respuestas
    
    Arquitectura:
    - Embedding Layer (convierte palabras a vectores)
    - Positional Encoding (agrega información de posición)
    - N capas de Transformer Blocks
    - Capa de salida (genera siguiente palabra)
    """
    def __init__(
        self,
        vocab_size: int,
        d_model: int = 256,
        num_heads: int = 8,
        num_layers: int = 6,
        d_ff: int = 1024,
        max_len: int = 128,
        dropout: float = 0.1
    ):
        super().__init__()
        
        self.d_model = d_model
        self.vocab_size = vocab_size
        
        # Embedding de palabras
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len, dropout)
        
        # Stack de Transformer Blocks
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        # Capa de salida
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        
        # Inicializar pesos
        self._init_weights()
    
    def _init_weights(self):
        """Inicialización de pesos"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x, mask=None):
        """
        Forward pass del transformer
        
        Args:
            x: tensor de entrada (batch_size, seq_len) con índices de palabras
            mask: máscara opcional para atención
        
        Returns:
            logits de salida (batch_size, seq_len, vocab_size)
        """
        # Embedding y escalado
        x = self.embedding(x) * np.sqrt(self.d_model)
        
        # Agregar codificación posicional
        x = self.pos_encoding(x)
        
        # Pasar por bloques transformer
        for transformer_block in self.transformer_blocks:
            x = transformer_block(x, mask)
        
        # Capa de salida
        output = self.fc_out(x)
        
        return output
    
    def generate(self, input_ids, max_length=100, temperature=0.8, top_k=50):
        """
        Genera texto autoregresivamente
        
        Args:
            input_ids: secuencia de entrada
            max_length: longitud máxima de generación
            temperature: controla aleatoriedad (mayor = más aleatorio)
            top_k: considera solo las top-k palabras más probables
        
        Returns:
            secuencia generada
        """
        self.eval()
        generated = input_ids.clone()
        
        with torch.no_grad():
            for _ in range(max_length):
                # Predecir siguiente token
                outputs = self.forward(generated)
                
                # Obtener logits de la última posición
                next_token_logits = outputs[:, -1, :] / temperature
                
                # Aplicar top-k filtering
                if top_k > 0:
                    indices_to_remove = next_token_logits < torch.topk(next_token_logits, top_k)[0][..., -1, None]
                    next_token_logits[indices_to_remove] = -float('Inf')
                
                # Muestrear siguiente token
                probs = torch.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                
                # Agregar a secuencia generada
                generated = torch.cat([generated, next_token], dim=1)
                
                # Detener si generamos token de fin
                if next_token.item() == 2:  # <EOS> token
                    break
        
        return generated


# =============================================================================
# CHATBOT CON TRANSFORMER
# =============================================================================

class PetStoreBotTransformer:
    """
    Chatbot Inteligente con Transformer para Pet Store
    
    Utiliza arquitectura Transformer para generar respuestas contextuales
    basadas en el mensaje del usuario y datos de la base de datos.
    """
    
    def __init__(self):
        self.db = PetStoreDatabase()
        self.predictor = PetStorePredictor()
        
        # Configuración del modelo
        self.d_model = 256
        self.num_heads = 8
        self.num_layers = 4
        self.d_ff = 1024
        self.max_len = 128
        self.dropout = 0.1
        
        # Vocabulario y tokenización
        self.vocab = None
        self.word2idx = None
        self.idx2word = None
        self.vocab_size = 0
        
        # Modelo transformer
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Tokens especiales
        self.PAD_TOKEN = '<PAD>'
        self.SOS_TOKEN = '<SOS>'
        self.EOS_TOKEN = '<EOS>'
        self.UNK_TOKEN = '<UNK>'
        
        # Intentar cargar modelo entrenado
        self.model_trained = False
        try:
            self.cargar_modelo()
            logger.info(" Modelo Transformer cargado exitosamente")
        except Exception as e:
            logger.warning(f"  Modelo Transformer no encontrado: {e}")
            logger.info("   Se usará modo híbrido con respuestas predefinidas")
    
    def construir_vocabulario(self, textos: List[str]):
        """
        Construye vocabulario a partir de textos de entrenamiento
        """
        from collections import Counter
        import re
        
        # Tokenizar todos los textos
        words = []
        for texto in textos:
            texto = texto.lower()
            texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
            words.extend(texto.split())
        
        # Contar frecuencias
        word_counts = Counter(words)
        
        # Crear vocabulario (palabras más frecuentes)
        vocab_list = [self.PAD_TOKEN, self.SOS_TOKEN, self.EOS_TOKEN, self.UNK_TOKEN]
        vocab_list += [word for word, _ in word_counts.most_common(5000)]
        
        self.vocab = vocab_list
        self.word2idx = {word: idx for idx, word in enumerate(vocab_list)}
        self.idx2word = {idx: word for word, idx in self.word2idx.items()}
        self.vocab_size = len(vocab_list)
        
        logger.info(f"Vocabulario construido: {self.vocab_size} palabras")
    
    def texto_a_indices(self, texto: str, max_len: Optional[int] = None) -> torch.Tensor:
        """
        Convierte texto a secuencia de índices
        """
        import re
        
        if max_len is None:
            max_len = self.max_len
        
        # Normalizar texto
        texto = texto.lower()
        texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
        palabras = texto.split()
        
        # Convertir a índices
        indices = [self.word2idx.get(self.SOS_TOKEN, 1)]
        for palabra in palabras[:max_len-2]:
            idx = self.word2idx.get(palabra, self.word2idx[self.UNK_TOKEN])
            indices.append(idx)
        indices.append(self.word2idx.get(self.EOS_TOKEN, 2))
        
        # Padding
        while len(indices) < max_len:
            indices.append(self.word2idx.get(self.PAD_TOKEN, 0))
        
        return torch.tensor(indices[:max_len], dtype=torch.long)
    
    def indices_a_texto(self, indices: torch.Tensor) -> str:
        """
        Convierte secuencia de índices a texto
        """
        palabras = []
        for idx in indices:
            idx = idx.item() if torch.is_tensor(idx) else idx
            palabra = self.idx2word.get(idx, self.UNK_TOKEN)
            
            if palabra == self.EOS_TOKEN:
                break
            if palabra not in [self.PAD_TOKEN, self.SOS_TOKEN]:
                palabras.append(palabra)
        
        return ' '.join(palabras)
    
    def generar_respuesta_con_contexto(self, mensaje: str) -> Tuple[str, float]:
        """
        Genera respuesta usando el transformer con contexto de la base de datos
        
        Args:
            mensaje: mensaje del usuario
        
        Returns:
            tupla (respuesta, confianza)
        """
        # Si el modelo no está entrenado, usar respuestas híbridas
        if not self.model_trained or self.model is None:
            return self.generar_respuesta_hibrida(mensaje)
        
        try:
            # Convertir mensaje a tensor
            input_tensor = self.texto_a_indices(mensaje).unsqueeze(0).to(self.device)
            
            # Generar respuesta con el transformer
            self.model.eval()
            with torch.no_grad():
                output_indices = self.model.generate(
                    input_tensor,
                    max_length=80,
                    temperature=0.7,
                    top_k=40
                )
            
            # Convertir a texto
            respuesta = self.indices_a_texto(output_indices[0])
            
            # Enriquecer con datos si es necesario
            respuesta_enriquecida = self.enriquecer_respuesta(mensaje, respuesta)
            
            return respuesta_enriquecida, 0.85
            
        except Exception as e:
            logger.error(f"Error generando respuesta con transformer: {e}")
            return self.generar_respuesta_hibrida(mensaje)
    
    def generar_respuesta_hibrida(self, mensaje: str) -> Tuple[str, float]:
        """
        Genera respuesta híbrida combinando patrones y datos
        
        Usado como fallback cuando el transformer no está disponible
        Usa el sistema de detección de intenciones del chatbot original
        """
        import re
        mensaje_lower = mensaje.lower()
        
        # Normalizar texto
        texto_norm = re.sub(r'[^a-záéíóúñü\s0-9]', '', mensaje_lower)
        texto_norm = re.sub(r'\s+', ' ', texto_norm).strip()
        
        # === SALUDOS ===
        if any(palabra in texto_norm for palabra in ['hola', 'buenos', 'buenas', 'hey', 'saludos']):
            respuestas = [
                "¡Hola!  Soy tu asistente virtual con IA. ¿En qué puedo ayudarte?",
                "¡Bienvenido! Estoy aquí para ayudarte con información del Pet Store.",
                "¡Hola! Pregúntame sobre mascotas, citas, estadísticas o predicciones."
            ]
            import random
            return random.choice(respuestas), 0.95
        
        # === DESPEDIDAS ===
        if any(palabra in texto_norm for palabra in ['adios', 'chao', 'hasta luego', 'bye', 'gracias']):
            respuestas = [
                "¡Hasta pronto!  Cuida bien a tus mascotas ",
                "¡Adiós! Regresa cuando necesites ayuda.",
                "¡Nos vemos! Que tengas un excelente día."
            ]
            import random
            return random.choice(respuestas), 0.95
        
        # === BÚSQUEDA DE MASCOTA (alta prioridad) ===
        if any(palabra in texto_norm for palabra in ['buscar mascota', 'busca mascota', 'buscar la mascota', 'busca la mascota', 'busca un mascota', 'busca una mascota', 'informacion de la mascota', 'informacion sobre la mascota', 'datos de la mascota', 'mascota llamada', 'mascota corona', 'busqueda de la mascota']):
            # Extraer nombre de la mascota
            import re
            # Intentar extraer el nombre después de palabras clave
            patrones = [
                r'mascota\s+(?:llamada|llamado|de\s+nombre)?\s*(\w+)',
                r'busca\s+(?:la\s+)?(?:mascota\s+)?(\w+)',
                r'informacion\s+(?:de|sobre)\s+(?:la\s+)?mascota\s+(\w+)'
            ]
            
            nombre = None
            for patron in patrones:
                match = re.search(patron, texto_norm, re.IGNORECASE)
                if match:
                    nombre = match.group(1)
                    break
            
            if nombre:
                df = self.db.buscar_mascota_por_nombre(nombre)
                if df.empty:
                    respuesta = f" No se encontró ninguna mascota con el nombre '{nombre}'.\n\n"
                    respuesta += " **Sugerencias:**\n"
                    respuesta += "• Verifica la ortografía\n"
                    respuesta += "• Intenta con solo el nombre (sin apellidos)\n"
                    respuesta += "• Usa el formato: 'buscar mascota [nombre]'"
                    return respuesta, 0.85
                
                respuesta = f" **RESULTADOS DE BÚSQUEDA: '{nombre}'**\n\n"
                for idx, row in df.iterrows():
                    respuesta += f" **{row['nombre']}** (ID: {row['pet_id']})\n"
                    respuesta += f"   • Tipo: {row['tipo']}\n"
                    respuesta += f"   • Raza: {row['raza']}\n"
                    respuesta += f"   • Edad: {row['edad']} años | Sexo: {row['sexo']}\n"
                    respuesta += f"   • Propietario: {row['propietario']}\n"
                    respuesta += f"   • Contacto: {row['telefono']}\n\n"
                return respuesta, 0.92
            else:
                respuesta = " Por favor proporciona el nombre de la mascota.\n\n"
                respuesta += "**Ejemplos:**\n"
                respuesta += "• 'buscar mascota Max'\n"
                respuesta += "• 'información de la mascota Luna'\n"
                respuesta += "• 'mascota llamada Bobby'"
                return respuesta, 0.75
        
        # === ESTADÍSTICAS (prioridad antes de otras, pero después de búsqueda) ===
        # NOTA: Excluir cuando dice explícitamente "predicciones"
        if (any(palabra in texto_norm for palabra in ['estadistica', 'estadisticas', 'metricas', 'reporte', 'resumen', 'numeros', 'cifras']) and 
            not any(palabra in texto_norm for palabra in ['prediccion', 'predicciones', 'predecir', 'pronostico'])):
            stats = self.db.obtener_estadisticas_generales()
            respuesta = f""" **Estadísticas del Sistema:**

             Mascotas registradas: {stats['total_mascotas']}
             Clientes activos: {stats['total_clientes']}
             Total de citas: {stats['total_citas']}
             Servicios disponibles: {stats['total_servicios']}

            ¿Necesitas más detalles sobre alguna métrica específica?"""
            return respuesta, 0.92
        
        # === CITAS ===
        if any(palabra in texto_norm for palabra in ['citas', 'cita', 'hoy', 'agenda', 'programadas', 'consultar citas y programacion', 'consultar citas']):
            df = self.db.obtener_citas_hoy()
            total = len(df)
            if total > 0:
                respuesta = f" **CITAS PROGRAMADAS HOY ({datetime.now().strftime('%d/%m/%Y')})**\n\n"
                respuesta += f"Total de citas: {total}\n\n"
                for idx, row in df.head(5).iterrows():
                    hora = f"{int(row['hora']):02d}:00"
                    respuesta += f" **{hora}** - {row['mascota']} ({row['tipo_mascota']})\n"
                    respuesta += f"   • Cliente: {row['cliente']}\n"
                    respuesta += f"   • Servicio: {row['servicio']}\n\n"
                if total > 5:
                    respuesta += f"... y {total - 5} citas más.\n"
            else:
                respuesta = " No hay citas programadas para hoy. Es un día tranquilo."
            return respuesta, 0.92
        
        # === VENTAS ===
        if any(palabra in texto_norm for palabra in ['ventas', 'venta', 'vendido', 'ingresos', 'transacciones', 'analisis de ventas']):
            ventas_dia = self.db.obtener_ventas_dia()
            ventas_mes = self.db.obtener_ventas_mes()
            comparativa = self.db.obtener_comparativa_ventas_mensual()
            
            respuesta = " **REPORTE DE VENTAS**\n\n"
            respuesta += " **Ventas del Día:**\n"
            respuesta += f"   • Total: ${ventas_dia['total_ventas']:,.2f}\n"
            respuesta += f"   • Transacciones: {ventas_dia['total_transacciones']}\n"
            respuesta += f"   • Items vendidos: {ventas_dia['total_items_vendidos']}\n\n"
            
            respuesta += " **Ventas del Mes:**\n"
            respuesta += f"   • Total: ${ventas_mes['total_ventas']:,.2f}\n"
            respuesta += f"   • Transacciones: {ventas_mes['total_transacciones']}\n\n"
            
            if comparativa['tendencia'] == 'crecimiento':
                emoji = ''
            elif comparativa['tendencia'] == 'decrecimiento':
                emoji = ''
            else:
                emoji = ''
            
            respuesta += f"{emoji} **Tendencia:** {comparativa['tendencia'].upper()}\n"
            respuesta += f"   • Cambio: {comparativa['porcentaje_cambio']:+.2f}%"
            
            return respuesta, 0.92
        
        # === TIPO DE MASCOTA MÁS COMÚN ===
        if ('tipo' in texto_norm and 'mascota' in texto_norm) or ('mascota' in texto_norm and any(p in texto_norm for p in ['comun', 'frecuente', 'popular'])):
            df = self.db.obtener_dataset_completo()
            if not df.empty:
                analisis = self.predictor.analizar_tipo_mascota_mas_comun(df)
                respuesta = f" **ANÁLISIS: Tipo de Mascota Más Común**\n\n"
                respuesta += f" El tipo más común es: **{analisis['tipo_mas_comun']}**\n\n"
                respuesta += " **Distribución completa:**\n"
                for stat in analisis['estadisticas'][:5]:
                    barra = "" * int(stat['porcentaje'] / 5)
                    respuesta += f"• {stat['tipo']}: {stat['cantidad']} ({stat['porcentaje']}%) {barra}\n"
                return respuesta, 0.92
            else:
                return " No hay datos suficientes para realizar el análisis.", 0.70
        
        # === PRODUCTOS E INVENTARIO ===
        if any(palabra in texto_norm for palabra in ['productos', 'producto', 'inventario', 'stock']):
            cantidad = self.db.obtener_cantidad_productos()
            bajo_inventario = self.db.obtener_alerta_bajo_inventario()
            
            respuesta = " **INFORMACIÓN DE INVENTARIO**\n\n"
            respuesta += f"**Total de productos:** {cantidad}\n\n"
            
            if not bajo_inventario.empty:
                respuesta += f" **ALERTAS DE BAJO INVENTARIO:** {len(bajo_inventario)} productos\n\n"
                respuesta += "**Top 5 productos con menos stock:**\n"
                for idx, row in bajo_inventario.head(5).iterrows():
                    respuesta += f"• **{row['producto']}** ({row['categoria']})\n"
                    respuesta += f"  Stock actual: {int(row['stock_actual'])} | Mínimo: {int(row['stock_minimo'])}\n"
            else:
                respuesta += " No hay alertas de bajo inventario."
            
            return respuesta, 0.90
        
        # === ALERTAS Y VENCIMIENTOS ===
        if any(palabra in texto_norm for palabra in ['alerta', 'alertas', 'vencimiento', 'vencer', 'proximos a vencer']):
            productos_vencer = self.db.obtener_productos_proximos_vencer(30)
            bajo_inventario = self.db.obtener_alerta_bajo_inventario()
            
            respuesta = " **ALERTAS DEL SISTEMA**\n\n"
            
            if not productos_vencer.empty:
                respuesta += f" **PRODUCTOS PRÓXIMOS A VENCER:** {len(productos_vencer)}\n\n"
                criticos = productos_vencer[productos_vencer['dias_hasta_vencer'] <= 7]
                if not criticos.empty:
                    respuesta += " **CRÍTICOS ( 7 días):**\n"
                    for idx, row in criticos.head(3).iterrows():
                        respuesta += f"• {row['producto']} - {int(row['dias_hasta_vencer'])} días\n"
                    respuesta += "\n"
            else:
                respuesta += " No hay productos próximos a vencer.\n\n"
            
            if not bajo_inventario.empty:
                respuesta += f" **BAJO INVENTARIO:** {len(bajo_inventario)} productos\n"
            else:
                respuesta += " No hay alertas de bajo inventario."
            
            return respuesta, 0.90
        
        # === PREDICCIONES ===
        if any(palabra in texto_norm for palabra in ['predice', 'prediccion', 'predicciones', 'pronostico', 'dame predicciones', 'dame prediciones', 'predicciones con machine learning']):
            if not self.predictor.trained:
                respuesta = """ **Los modelos predictivos aún no están entrenados**

                    Para activar las predicciones con red neuronal:

                    **Opción 1: Desde la API**
                    ```
                    POST http://localhost:8000/api/entrenar
                    ```

                    **Opción 2: Desde terminal**
                    ```bash
                    python entrenar_modelos.py
                    ```

                    ⏱ Tiempo estimado: 5-10 minutos

                    Mientras tanto, puedo ayudarte con:
                     Estadísticas actuales
                     Citas programadas
                     Análisis de ventas
                     Tipo de mascota más común (análisis sin ML)
                    """
                return respuesta, 0.85
            
            ahora = datetime.now()
            dia_semana = ahora.weekday()
            hora_dia = ahora.hour
            mes = ahora.month
            
            prediccion = self.predictor.predecir_tipo_mascota(dia_semana, hora_dia, mes, 1)
            
            dias_nombre = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            
            respuesta = f" **PREDICCIÓN: Tipo de Mascota**\n\n"
            respuesta += f" Día: {dias_nombre[dia_semana]}\n"
            respuesta += f"⏰ Hora: {hora_dia}:00\n\n"
            respuesta += f" **Predicción:** {prediccion['tipo_mas_probable']}\n"
            respuesta += f" **Confianza:** {prediccion['confianza']:.1%}\n\n"
            respuesta += "**Top 3 más probables:**\n"
            for pred in prediccion['predicciones'][:3]:
                respuesta += f"• {pred['tipo_mascota']}: {pred['probabilidad']:.1%}\n"
            
            return respuesta, 0.90
        
        # === CLUSTERING ===
        if any(palabra in texto_norm for palabra in ['clustering', 'cluster', 'agrupar', 'segmentar', 'segmentacion']):
            try:
                df = self.db.obtener_dataset_completo()
                if df.empty:
                    return " No hay datos suficientes para realizar clustering.", 0.70
                
                analisis = self.predictor.analisis_clustering_completo(df)
                respuesta = " **ANÁLISIS DE HIERARCHICAL CLUSTERING**\n\n"
                
                if "clustering_clientes" in analisis and "error" not in analisis['clustering_clientes']:
                    cc = analisis['clustering_clientes']
                    respuesta += f" **SEGMENTACIÓN DE CLIENTES:** {cc['n_segmentos']} segmentos\n\n"
                    for segmento in cc['segmentos'][:3]:
                        respuesta += f"   **{segmento['nombre']}:**\n"
                        respuesta += f"   • Clientes: {segmento['total_clientes']}\n"
                        respuesta += f"   • Gasto promedio: ${segmento['gasto_promedio']:.2f}\n\n"
                
                return respuesta, 0.88
            except:
                return " Error al generar clustering. Verifica que haya datos suficientes.", 0.60
        
        # === SERVICIOS ===
        if any(palabra in texto_norm for palabra in ['servicios', 'servicio', 'que servicios', 'lista de servicios']):
            df = self.db.obtener_servicios_disponibles()
            if df.empty:
                return " No se encontraron servicios disponibles.", 0.70
            
            respuesta = " **SERVICIOS DISPONIBLES:**\n\n"
            for idx, row in df.head(10).iterrows():
                respuesta += f"• **{row['nombre']}**\n"
                if row['descripcion']:
                    respuesta += f"  {row['descripcion']}\n"
                respuesta += f"   Precio: ${row['precio']:,.2f}"
                if row['duracion_minutos']:
                    respuesta += f" | ⏱ {row['duracion_minutos']} min"
                respuesta += "\n\n"
            
            return respuesta, 0.90
        
        # === INFORMACIÓN VETERINARIA GENÉRICA ===
        if any(palabra in texto_norm for palabra in ['informacion veterinaria', 'info veterinaria', 'informacion de mascota', 'informacion sobre mascota']) and not any(palabra in texto_norm for palabra in ['buscar', 'busca', 'llamada']):
            respuesta = """ **INFORMACIÓN VETERINARIA DISPONIBLE**

            Puedo ayudarte con:

            **Enfermedades:**
            • "qué es moquillo" - Información sobre moquillo canino
            • "qué es parvovirus" - Información sobre parvovirus
            • "qué es rabia" - Información sobre rabia
            • "leucemia felina" - Información sobre FeLV

            **Prevención:**
            • "vacunas" - Calendario de vacunación completo
            • "desparasitación" - Guía de desparasitación

            **Cuidados:**
            • "alimentación" - Consejos de alimentación
            • "cuidados" - Cuidados generales

            **Emergencias:**
            • "emergencia" - Guía de emergencias veterinarias

            **Ejemplos:**
            "¿Qué es el moquillo?"
            "Calendario de vacunas"
            "¿Cómo alimentar a mi cachorro?"

            ¿Sobre qué tema necesitas información?"""
            return respuesta, 0.90
        
        # === INFORMACIÓN VETERINARIA ESPECÍFICA ===
        
        # Moquillo
        if any(palabra in texto_norm for palabra in ['moquillo', 'distemper', 'que es moquillo']):
            respuesta = """ **MOQUILLO CANINO**

            El moquillo es una enfermedad viral grave que afecta a perros.

            **Síntomas:**
            • Fiebre alta
            • Secreción nasal y ocular
            • Tos y dificultad respiratoria
            • Vómitos y diarrea
            • Letargo y falta de apetito
            • En casos avanzados: convulsiones

            **Prevención:**
             Vacunación (parte de la vacuna múltiple)
             Refuerzos anuales
             Evitar contacto con perros enfermos

            **Tratamiento:**
             Requiere atención veterinaria URGENTE
            No hay cura específica, se trata sintomáticamente

             ¿Necesitas agendar una cita de urgencia?"""
            return respuesta, 0.95
        
        # Parvovirus
        if any(palabra in texto_norm for palabra in ['parvovirus', 'parvo', 'parvoviral']):
            respuesta = """ **PARVOVIRUS CANINO**

            Enfermedad viral muy contagiosa que afecta principalmente a cachorros.

            **Síntomas:**
            • Diarrea severa (a menudo con sangre)
            • Vómitos intensos
            • Fiebre
            • Letargo extremo
            • Pérdida de apetito
            • Deshidratación rápida

            **Prevención:**
             Vacunación temprana (6-8 semanas)
             Refuerzos según calendario
             Evitar lugares con perros hasta completar vacunas

            **Emergencia:**
             REQUIERE ATENCIÓN VETERINARIA INMEDIATA
            La deshidratación puede ser mortal en 24-48 horas

             Si sospechas parvo, llama YA a tu veterinario"""
            return respuesta, 0.95
        
        # Vacunas
        if any(palabra in texto_norm for palabra in ['vacuna', 'vacunas', 'vacunar', 'inmunizacion']):
            respuesta = """ **INFORMACIÓN SOBRE VACUNAS**

             **PERROS - Vacunas esenciales:**

            **Cachorros (6-16 semanas):**
            • 6-8 sem: Primera vacuna múltiple
            • 10-12 sem: Segunda dosis
            • 14-16 sem: Tercera dosis + Rabia

            **Adultos (Anual):**
            • Refuerzo múltiple
            • Rabia (cada 1-3 años según vacuna)

             **GATOS - Vacunas esenciales:**

            **Gatitos (6-16 semanas):**
            • 6-8 sem: Primera triple felina
            • 10-12 sem: Segunda dosis
            • 14-16 sem: Tercera dosis + Rabia

            **Adultos (Anual):**
            • Refuerzo triple felina
            • Rabia

             **Importante:** Mantén el calendario al día para proteger a tu mascota"""
            return respuesta, 0.95
        
        # Desparasitación
        if any(palabra in texto_norm for palabra in ['desparasitar', 'desparasitacion', 'parasito', 'parasitos', 'gusano', 'gusanos']):
            respuesta = """ **DESPARASITACIÓN**

             **Calendario recomendado:**

            **Cachorros/Gatitos:**
            • 2, 4, 6, 8 semanas de edad
            • Luego mensual hasta los 6 meses
            • Después cada 3-6 meses

            **Adultos:**
            • Cada 3-6 meses
            • Cada 3 meses si tiene acceso al exterior

             **Señales de parásitos:**
            • Diarrea o vómito
            • Abdomen hinchado
            • Pérdida de peso
            • Picazón anal (se arrastra)
            • Gusanos visibles en heces

             **Importante:** Usa productos recomendados por veterinario"""
            return respuesta, 0.95
        
        # Alimentación
        if any(palabra in texto_norm for palabra in ['alimentacion', 'comida', 'comer', 'dieta', 'alimento']):
            respuesta = """ **ALIMENTACIÓN PARA MASCOTAS**

             **PERROS:**

            **Cachorros:** 3-4 comidas al día, alimento especial para cachorros
            **Adultos:** 2 comidas al día, alimento balanceado
            **Mayores (>7 años):** Alimento senior, menor grasa

             **GATOS:**

            **Gatitos:** 3-4 comidas pequeñas, alto en proteínas
            **Adultos:** 2-3 comidas al día, alimento balanceado
            **Agua fresca siempre disponible**

             **NUNCA les des:**
            • Chocolate
            • Cebolla/Ajo
            • Uvas/Pasas
            • Aguacate
            • Huesos cocidos

             Consulta con tu veterinario para recomendaciones específicas"""
            return respuesta, 0.93
        
        # Emergencia
        if any(palabra in texto_norm for palabra in ['emergencia', 'urgente', 'grave', 'ayuda']):
            respuesta = """ **EMERGENCIA VETERINARIA**

             **ACTÚA RÁPIDO - Lleva a tu mascota al veterinario INMEDIATAMENTE si:**

             **EMERGENCIAS CRÍTICAS:**
            • Dificultad para respirar
            • Sangrado que no para
            • Convulsiones
            • Pérdida de conciencia
            • Trauma severo
            • Abdomen hinchado y duro
            • Intoxicación conocida

             **MIENTRAS LLEGAS AL VETERINARIO:**
            1. Mantén la calma
            2. Transporte seguro
            3. No des medicamentos
            4. Llama antes de ir

            ⏱ **En emergencias, CADA MINUTO CUENTA**"""
            return respuesta, 0.95
        
        # Ayuda
        if 'ayuda' in texto_norm or 'help' in texto_norm or 'que puedes' in texto_norm or 'comandos' in texto_norm:
            respuesta = """ **COMANDOS DISPONIBLES:**

             **BÚSQUEDA:**
            • "buscar mascota [nombre]" - Buscar por nombre
            • "información de la mascota [nombre]"
            • "mascota llamada [nombre]"

             **ESTADÍSTICAS Y ANÁLISIS:**
            • "estadísticas" - Estadísticas generales
            • "tipo más común" - Tipo de mascota más común
            • "citas hoy" - Citas programadas

             **MÉTRICAS DE NEGOCIO:**
            • "ventas" - Reporte de ventas
            • "alertas" - Alertas de inventario
            • "productos" - Info de inventario

             **INFORMACIÓN VETERINARIA:**
            • "qué es moquillo" - Info sobre moquillo
            • "qué es parvovirus" - Info sobre parvovirus
            • "vacunas" - Calendario de vacunación
            • "desparasitación" - Guía de desparasitación
            • "alimentación" - Consejos de alimentación

             **ANÁLISIS CON IA:**
            • "predicciones" - Predicción con IA
            • "clustering" - Segmentación de clientes

            **Ejemplos:**
            "buscar mascota Corona"
            "¿Cuántas citas hay hoy?"
            "¿Qué es el parvovirus?"
            "Alertas de inventario"
            """
            return respuesta, 0.90
        
        # Respuesta por defecto
        respuesta = """¡Hola!  Soy tu asistente virtual con IA.

        Puedo ayudarte con:
         Buscar mascotas por nombre
         Estadísticas y métricas del negocio
         Consultar citas y programación  
         Análisis de ventas
         Información veterinaria (moquillo, vacunas, etc.)
         Predicciones con machine learning

        **Ejemplos de preguntas:**
        • "buscar mascota Corona"
        • "estadísticas"
        • "citas hoy"
        • "qué es el moquillo"
        • "predicciones"

        Escribe "ayuda" para ver todos los comandos disponibles.

        ¿Qué necesitas?"""
        
        return respuesta, 0.70
    
    def enriquecer_respuesta(self, mensaje: str, respuesta_base: str) -> str:
        """
        Enriquece la respuesta del transformer con datos reales de la BD
        """
        mensaje_lower = mensaje.lower()
        
        # Si menciona estadísticas, agregar datos reales
        if 'estadistica' in mensaje_lower or 'metrica' in mensaje_lower:
            stats = self.db.obtener_estadisticas_generales()
            respuesta_base += f"\n\n Datos actuales:\n"
            respuesta_base += f"• Mascotas: {stats['total_mascotas']}\n"
            respuesta_base += f"• Clientes: {stats['total_clientes']}\n"
            respuesta_base += f"• Citas: {stats['total_citas']}"
        
        return respuesta_base
    
    def procesar_mensaje(self, mensaje: str) -> Dict:
        """
        Procesa mensaje y genera respuesta usando Transformer
        
        Returns:
            Dict con respuesta, intención, confianza y timestamp
        """
        # Utilizo el modelo Transformer para generar una respuesta contextual al mensaje del usuario
        respuesta, confianza = self.generar_respuesta_con_contexto(mensaje)
        
        # Creo un diccionario con toda la información de la respuesta generada para el frontend
        return {
            "respuesta": respuesta,  # Texto de la respuesta que el chatbot generó para el usuario
            "intencion": "transformer_generation",  # Indico que la respuesta fue generada por el modelo Transformer
            "confianza": confianza,  # Nivel de confianza del modelo en su respuesta (0-1, donde 1 es máxima confianza)
            "timestamp": datetime.now().isoformat(),  # Registro la fecha y hora exacta cuando se generó la respuesta
            "modelo": "Transformer" if self.model_trained else "Híbrido"  # Identifico qué modelo se usó (Transformer si está entrenado, Híbrido si no)
        }
    
    def guardar_modelo(self, ruta='models/'):
        """Guarda el modelo transformer"""
        os.makedirs(ruta, exist_ok=True)
        
        if self.model is not None:
            torch.save({
                'model_state': self.model.state_dict(),
                'vocab': self.vocab,
                'word2idx': self.word2idx,
                'idx2word': self.idx2word,
                'vocab_size': self.vocab_size,
                'config': {
                    'd_model': self.d_model,
                    'num_heads': self.num_heads,
                    'num_layers': self.num_layers,
                    'd_ff': self.d_ff,
                    'max_len': self.max_len,
                    'dropout': self.dropout
                }
            }, os.path.join(ruta, 'transformer_chatbot.pth'))
            
            logger.info(" Modelo Transformer guardado")
    
    def cargar_modelo(self, ruta='models/transformer_chatbot.pth'):
        """Carga el modelo transformer"""
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Modelo no encontrado en {ruta}")
        
        checkpoint = torch.load(ruta, map_location=self.device)
        
        # Cargar vocabulario
        self.vocab = checkpoint['vocab']
        self.word2idx = checkpoint['word2idx']
        self.idx2word = checkpoint['idx2word']
        self.vocab_size = checkpoint['vocab_size']
        
        # Cargar configuración
        config = checkpoint['config']
        self.d_model = config['d_model']
        self.num_heads = config['num_heads']
        self.num_layers = config['num_layers']
        self.d_ff = config['d_ff']
        self.max_len = config['max_len']
        self.dropout = config['dropout']
        
        # Crear y cargar modelo
        self.model = TransformerChatbot(
            vocab_size=self.vocab_size,
            d_model=self.d_model,
            num_heads=self.num_heads,
            num_layers=self.num_layers,
            d_ff=self.d_ff,
            max_len=self.max_len,
            dropout=self.dropout
        ).to(self.device)
        
        self.model.load_state_dict(checkpoint['model_state'])
        self.model.eval()
        self.model_trained = True
        
        logger.info(f" Modelo Transformer cargado desde {ruta}")


# =============================================================================
# EJEMPLO DE USO
# =============================================================================
if __name__ == "__main__":
    print(" Chatbot con Transformer - Pet Store")
    print("=" * 60)
    
    bot = PetStoreBotTransformer()
    
    # Ejemplos de mensajes
    ejemplos = [
        "Hola, ¿cómo estás?",
        "Muéstrame las estadísticas",
        "¿Cuántas citas hay hoy?",
        "¿Cuál es el tipo de mascota más común?",
        "Dame el reporte de ventas"
    ]
    
    for mensaje in ejemplos:
        print(f"\n Usuario: {mensaje}")
        resultado = bot.procesar_mensaje(mensaje)
        print(f" Bot ({resultado['modelo']}): {resultado['respuesta']}")
        print(f"   Confianza: {resultado['confianza']:.0%}")

