/**
 * EJEMPLO DE USO DEL CHATBOT TRANSFORMER DESDE FRONTEND
 * 
 * Este archivo muestra cómo integrar el chatbot con Transformer
 * en tu aplicación React, Vue, o JavaScript vanilla
 */

// =============================================================================
// CONFIGURACIÓN
// =============================================================================

const API_BASE_URL = 'http://localhost:8000';
const CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;

// =============================================================================
// FUNCIÓN PRINCIPAL PARA ENVIAR MENSAJES
// =============================================================================

/**
 * Envía un mensaje al chatbot con Transformer
 * 
 * @param {string} mensaje - El mensaje del usuario
 * @param {string} usuarioId - ID del usuario (opcional)
 * @param {boolean} useTransformer - Usar Transformer (true) o LSTM (false)
 * @returns {Promise<Object>} Respuesta del chatbot
 */
async function enviarMensaje(mensaje, usuarioId = 'anonymous', useTransformer = true) {
    try {
        const response = await fetch(`${CHAT_ENDPOINT}?use_transformer=${useTransformer}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mensaje: mensaje,
                usuario_id: usuarioId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error('Error al comunicarse con el chatbot:', error);
        throw error;
    }
}

// =============================================================================
// EJEMPLOS DE USO
// =============================================================================

/**
 * Ejemplo 1: Consulta simple
 */
async function ejemplo1_consultaSimple() {
    console.log('📝 Ejemplo 1: Consulta Simple\n');
    
    const respuesta = await enviarMensaje("Hola, ¿cómo estás?");
    
    console.log('👤 Usuario:', "Hola, ¿cómo estás?");
    console.log('🤖 Bot:', respuesta.respuesta);
    console.log('📊 Modelo:', respuesta.modelo);
    console.log('🎯 Confianza:', `${(respuesta.confianza * 100).toFixed(0)}%`);
    console.log('\n---\n');
}

/**
 * Ejemplo 2: Consulta de estadísticas
 */
async function ejemplo2_estadisticas() {
    console.log('📝 Ejemplo 2: Consulta de Estadísticas\n');
    
    const respuesta = await enviarMensaje("Muéstrame las estadísticas del sistema");
    
    console.log('👤 Usuario:', "Muéstrame las estadísticas del sistema");
    console.log('🤖 Bot:', respuesta.respuesta);
    console.log('\n---\n');
}

/**
 * Ejemplo 3: Múltiples consultas en secuencia
 */
async function ejemplo3_conversacion() {
    console.log('📝 Ejemplo 3: Conversación Múltiple\n');
    
    const preguntas = [
        "¿Cuántas citas hay hoy?",
        "¿Y cuánto vendimos?",
        "Dame el tipo de mascota más común"
    ];
    
    for (const pregunta of preguntas) {
        const respuesta = await enviarMensaje(pregunta);
        console.log('👤 Usuario:', pregunta);
        console.log('🤖 Bot:', respuesta.respuesta);
        console.log('');
    }
    
    console.log('---\n');
}

/**
 * Ejemplo 4: Comparar Transformer vs LSTM
 */
async function ejemplo4_comparacion() {
    console.log('📝 Ejemplo 4: Comparación Transformer vs LSTM\n');
    
    const mensaje = "¿Cuál es el tipo de mascota más común?";
    
    // Con Transformer
    const respuestaTransformer = await enviarMensaje(mensaje, 'user123', true);
    console.log('🤖 TRANSFORMER:');
    console.log(respuestaTransformer.respuesta);
    console.log(`Confianza: ${(respuestaTransformer.confianza * 100).toFixed(0)}%\n`);
    
    // Con LSTM
    const respuestaLSTM = await enviarMensaje(mensaje, 'user123', false);
    console.log('🤖 LSTM:');
    console.log(respuestaLSTM.respuesta);
    console.log(`Confianza: ${(respuestaLSTM.confianza * 100).toFixed(0)}%\n`);
    
    console.log('---\n');
}

// =============================================================================
// COMPONENTE REACT
// =============================================================================

/**
 * Ejemplo de componente React con el chatbot
 */
const ChatbotComponent = `
import React, { useState, useEffect, useRef } from 'react';

function ChatbotTransformer() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [useTransformer, setUseTransformer] = useState(true);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!inputMessage.trim()) return;

        // Agregar mensaje del usuario
        const userMessage = {
            type: 'user',
            content: inputMessage,
            timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setLoading(true);

        try {
            // Enviar al API
            const response = await fetch(
                \`http://localhost:8000/api/chat?use_transformer=\${useTransformer}\`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        mensaje: inputMessage,
                        usuario_id: 'react_user'
                    })
                }
            );

            const data = await response.json();

            // Agregar respuesta del bot
            const botMessage = {
                type: 'bot',
                content: data.respuesta,
                modelo: data.modelo,
                confianza: data.confianza,
                timestamp: data.timestamp
            };
            setMessages(prev => [...prev, botMessage]);

        } catch (error) {
            console.error('Error:', error);
            const errorMessage = {
                type: 'error',
                content: 'Error al comunicarse con el chatbot',
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chatbot-container">
            {/* Header */}
            <div className="chatbot-header">
                <h2>🤖 Chatbot con Transformer</h2>
                <div className="toggle-container">
                    <label>
                        <input
                            type="checkbox"
                            checked={useTransformer}
                            onChange={(e) => setUseTransformer(e.target.checked)}
                        />
                        Usar Transformer
                    </label>
                </div>
            </div>

            {/* Messages */}
            <div className="messages-container">
                {messages.map((msg, idx) => (
                    <div key={idx} className={\`message message-\${msg.type}\`}>
                        <div className="message-content">
                            {msg.content}
                        </div>
                        {msg.modelo && (
                            <div className="message-metadata">
                                {msg.modelo} • {(msg.confianza * 100).toFixed(0)}%
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div className="message message-bot loading">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="input-container">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Escribe tu mensaje..."
                    disabled={loading}
                />
                <button onClick={sendMessage} disabled={loading}>
                    {loading ? '⏳' : '📤'} Enviar
                </button>
            </div>
        </div>
    );
}

export default ChatbotTransformer;
`;

// =============================================================================
// COMPONENTE VUE
// =============================================================================

/**
 * Ejemplo de componente Vue con el chatbot
 */
const ChatbotVueComponent = `
<template>
  <div class="chatbot-container">
    <!-- Header -->
    <div class="chatbot-header">
      <h2>🤖 Chatbot con Transformer</h2>
      <div class="toggle-container">
        <label>
          <input type="checkbox" v-model="useTransformer" />
          Usar Transformer
        </label>
      </div>
    </div>

    <!-- Messages -->
    <div class="messages-container" ref="messagesContainer">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', \`message-\${msg.type}\`]"
      >
        <div class="message-content">{{ msg.content }}</div>
        <div v-if="msg.modelo" class="message-metadata">
          {{ msg.modelo }} • {{ (msg.confianza * 100).toFixed(0) }}%
        </div>
      </div>
      
      <div v-if="loading" class="message message-bot loading">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="input-container">
      <input
        type="text"
        v-model="inputMessage"
        @keypress.enter="sendMessage"
        placeholder="Escribe tu mensaje..."
        :disabled="loading"
      />
      <button @click="sendMessage" :disabled="loading">
        {{ loading ? '⏳' : '📤' }} Enviar
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatbotTransformer',
  data() {
    return {
      messages: [],
      inputMessage: '',
      loading: false,
      useTransformer: true,
      apiUrl: 'http://localhost:8000/api/chat'
    };
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return;

      // Agregar mensaje del usuario
      this.messages.push({
        type: 'user',
        content: this.inputMessage,
        timestamp: new Date().toISOString()
      });

      const mensaje = this.inputMessage;
      this.inputMessage = '';
      this.loading = true;

      try {
        const response = await fetch(
          \`\${this.apiUrl}?use_transformer=\${this.useTransformer}\`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              mensaje: mensaje,
              usuario_id: 'vue_user'
            })
          }
        );

        const data = await response.json();

        // Agregar respuesta del bot
        this.messages.push({
          type: 'bot',
          content: data.respuesta,
          modelo: data.modelo,
          confianza: data.confianza,
          timestamp: data.timestamp
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });

      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          type: 'error',
          content: 'Error al comunicarse con el chatbot',
          timestamp: new Date().toISOString()
        });
      } finally {
        this.loading = false;
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      container.scrollTop = container.scrollHeight;
    }
  }
};
</script>

<style scoped>
/* Estilos del componente */
.chatbot-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

.chatbot-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
}

.message {
  margin-bottom: 15px;
  padding: 10px 15px;
  border-radius: 8px;
  max-width: 80%;
}

.message-user {
  background: #667eea;
  color: white;
  margin-left: auto;
}

.message-bot {
  background: white;
  color: #333;
}

.message-error {
  background: #ff6b6b;
  color: white;
}

.message-metadata {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.input-container {
  display: flex;
  padding: 15px;
  background: white;
  border-top: 1px solid #ddd;
}

.input-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-container button {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-container button:hover {
  background: #5568d3;
}

.input-container button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  gap: 5px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}
</style>
`;

// =============================================================================
// CSS STYLING
// =============================================================================

const chatbotCSS = `
/* Estilos para el chatbot */
.chatbot-container {
    max-width: 600px;
    margin: 20px auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

.chatbot-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px 8px 0 0;
}

.messages-container {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background: #f5f5f5;
    border-left: 1px solid #ddd;
    border-right: 1px solid #ddd;
}

.message {
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 8px;
    max-width: 80%;
    animation: slideIn 0.3s ease-out;
}

.message-user {
    background: #667eea;
    color: white;
    margin-left: auto;
    text-align: right;
}

.message-bot {
    background: white;
    color: #333;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.message-metadata {
    font-size: 11px;
    color: #999;
    margin-top: 8px;
}

.input-container {
    display: flex;
    padding: 15px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 0 0 8px 8px;
}

.input-container input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
}

.input-container button {
    margin-left: 10px;
    padding: 12px 24px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s;
}

.input-container button:hover {
    background: #5568d3;
}

.input-container button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
`;

// =============================================================================
// EJECUTAR EJEMPLOS
// =============================================================================

async function ejecutarTodosLosEjemplos() {
    console.log('🚀 Ejecutando ejemplos de uso del Chatbot Transformer\n');
    console.log('=' .repeat(60) + '\n');
    
    try {
        await ejemplo1_consultaSimple();
        await ejemplo2_estadisticas();
        await ejemplo3_conversacion();
        await ejemplo4_comparacion();
        
        console.log('✅ Todos los ejemplos ejecutados correctamente\n');
        
    } catch (error) {
        console.error('❌ Error ejecutando ejemplos:', error);
    }
}

// Exportar para uso en otros archivos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        enviarMensaje,
        ChatbotComponent,
        ChatbotVueComponent,
        chatbotCSS,
        ejecutarTodosLosEjemplos
    };
}

// Si se ejecuta directamente con Node.js
if (typeof require !== 'undefined' && require.main === module) {
    ejecutarTodosLosEjemplos();
}

