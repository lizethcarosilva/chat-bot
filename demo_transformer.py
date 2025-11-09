"""
DEMO DEL CHATBOT TRANSFORMER
Script de demostración para probar el chatbot con Transformer
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transformer_chatbot import PetStoreBotTransformer
import time


def print_banner():
    """Imprime el banner de bienvenida"""
    print("\n" + "="*80)
    print(" DEMO: CHATBOT CON TRANSFORMER - PET STORE")
    print("="*80)
    print("\n Este chatbot usa arquitectura Transformer para generar respuestas")
    print("   Similar a GPT, con Multi-Head Attention y generación autoregresiva\n")
    print("Características:")
    print("   Respuestas contextuales y naturales")
    print("   Multi-Head Attention para entender mejor")
    print("   Enriquecimiento con datos en tiempo real")
    print("   Generación dinámica (no solo plantillas)\n")
    print("="*80 + "\n")


def demo_respuestas_automaticas():
    """
    Demo automático mostrando diferentes tipos de consultas
    """
    print("\n" + "="*80)
    print(" DEMO AUTOMÁTICO - Ejemplos de Consultas")
    print("="*80 + "\n")
    
    # Inicializar bot
    print(" Inicializando chatbot con Transformer...")
    bot = PetStoreBotTransformer()
    
    # Verificar estado del modelo
    if bot.model_trained:
        print(" Modelo Transformer cargado y listo\n")
    else:
        print("  Modo híbrido activo (sin transformer entrenado)")
        print("   Para entrenar el transformer: python entrenar_transformer.py\n")
    
    # Ejemplos de consultas
    ejemplos = [
        {
            "categoria": "Saludo",
            "mensaje": "Hola, ¿cómo estás?",
            "emoji": ""
        },
        {
            "categoria": "Estadísticas",
            "mensaje": "Muéstrame las estadísticas del sistema",
            "emoji": ""
        },
        {
            "categoria": "Citas",
            "mensaje": "¿Cuántas citas hay programadas para hoy?",
            "emoji": ""
        },
        {
            "categoria": "Ventas",
            "mensaje": "Dame el reporte de ventas del día",
            "emoji": ""
        },
        {
            "categoria": "Mascotas",
            "mensaje": "¿Cuál es el tipo de mascota más común?",
            "emoji": ""
        },
        {
            "categoria": "Inventario",
            "mensaje": "¿Hay productos próximos a vencer?",
            "emoji": ""
        },
        {
            "categoria": "Análisis",
            "mensaje": "¿Cómo va el negocio?",
            "emoji": ""
        },
        {
            "categoria": "Despedida",
            "mensaje": "Gracias por tu ayuda",
            "emoji": ""
        }
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'-'*80}")
        print(f"{ejemplo['emoji']} Ejemplo {i}/{len(ejemplos)}: {ejemplo['categoria']}")
        print(f"{'-'*80}\n")
        
        print(f" Usuario: {ejemplo['mensaje']}")
        
        # Procesar mensaje
        inicio = time.time()
        resultado = bot.procesar_mensaje(ejemplo['mensaje'])
        tiempo = time.time() - inicio
        
        # Mostrar respuesta
        print(f"\n Bot ({resultado['modelo']}):")
        print(resultado['respuesta'])
        print(f"\n Metadata:")
        print(f"   • Confianza: {resultado['confianza']:.0%}")
        print(f"   • Tiempo: {tiempo:.2f}s")
        print(f"   • Intención: {resultado['intencion']}")
        print(f"   • Timestamp: {resultado['timestamp']}")
        
        # Pausa entre ejemplos
        if i < len(ejemplos):
            time.sleep(1)
    
    print("\n" + "="*80)
    print(" Demo automático completado")
    print("="*80 + "\n")


def demo_interactivo():
    """
    Demo interactivo donde el usuario puede hacer preguntas
    """
    print("\n" + "="*80)
    print(" MODO INTERACTIVO - Chatea con el Bot")
    print("="*80 + "\n")
    
    # Inicializar bot
    bot = PetStoreBotTransformer()
    
    print(" Bot listo para conversar!")
    print("   Escribe tus preguntas o comandos:")
    print("   • 'salir' para terminar")
    print("   • 'ayuda' para ver comandos\n")
    
    historial = []
    
    while True:
        try:
            # Leer entrada
            mensaje = input(" Tú: ").strip()
            
            if not mensaje:
                continue
            
            # Comandos especiales
            if mensaje.lower() in ['salir', 'exit', 'quit', 'adios']:
                print("\n Bot: ¡Hasta pronto!  Cuida bien a tus mascotas \n")
                break
            
            if mensaje.lower() == 'historial':
                print("\n Historial de conversación:")
                for i, item in enumerate(historial[-5:], 1):
                    print(f"   {i}. Usuario: {item['mensaje']}")
                    print(f"      Bot: {item['respuesta'][:100]}...")
                print()
                continue
            
            # Procesar mensaje
            inicio = time.time()
            resultado = bot.procesar_mensaje(mensaje)
            tiempo = time.time() - inicio
            
            # Mostrar respuesta
            print(f"\n Bot ({resultado['modelo']}):")
            print(resultado['respuesta'])
            print(f"\n   [⏱ {tiempo:.2f}s |  Confianza: {resultado['confianza']:.0%}]\n")
            
            # Guardar en historial
            historial.append({
                'mensaje': mensaje,
                'respuesta': resultado['respuesta'],
                'confianza': resultado['confianza']
            })
            
        except KeyboardInterrupt:
            print("\n\n Bot: ¡Hasta pronto! \n")
            break
        except Exception as e:
            print(f"\n Error: {e}\n")
    
    # Resumen final
    if historial:
        print("\n" + "="*80)
        print(" RESUMEN DE LA CONVERSACIÓN")
        print("="*80)
        print(f"\n• Total de mensajes: {len(historial)}")
        print(f"• Confianza promedio: {sum(h['confianza'] for h in historial)/len(historial):.0%}")
        print("\n" + "="*80 + "\n")


def demo_comparacion():
    """
    Compara respuestas del Transformer vs respuestas clásicas
    """
    print("\n" + "="*80)
    print("  COMPARACIÓN: Transformer vs Sistema Clásico")
    print("="*80 + "\n")
    
    # Inicializar bot
    bot = PetStoreBotTransformer()
    
    # Mensaje de prueba
    mensaje = "¿Cuántas citas hay hoy?"
    
    print(f"Consulta: \"{mensaje}\"\n")
    print(f"{'-'*80}\n")
    
    # Procesar con Transformer
    print(" RESPUESTA TRANSFORMER:")
    resultado_transformer = bot.procesar_mensaje(mensaje)
    print(resultado_transformer['respuesta'])
    print(f"\n Confianza: {resultado_transformer['confianza']:.0%}")
    print(f" Modelo: {resultado_transformer['modelo']}")
    
    print(f"\n{'-'*80}\n")
    
    print(" El sistema Transformer ofrece:")
    print("   • Respuestas más naturales y contextuales")
    print("   • Enriquecimiento automático con datos reales")
    print("   • Capacidad de adaptarse a diferentes formas de preguntar")
    print("   • Generación dinámica (no solo plantillas)")
    
    print("\n" + "="*80 + "\n")


def main():
    """Función principal del demo"""
    print_banner()
    
    # Menú de opciones
    while True:
        print("Selecciona una opción:\n")
        print("  1⃣  Demo Automático (ejemplos predefinidos)")
        print("  2⃣  Modo Interactivo (chatea libremente)")
        print("  3⃣  Comparación de Modelos")
        print("  4⃣  Información del Sistema")
        print("  5⃣  Salir\n")
        
        opcion = input("Opción (1-5): ").strip()
        
        if opcion == '1':
            demo_respuestas_automaticas()
        elif opcion == '2':
            demo_interactivo()
        elif opcion == '3':
            demo_comparacion()
        elif opcion == '4':
            mostrar_info_sistema()
        elif opcion == '5':
            print("\n ¡Hasta luego!\n")
            break
        else:
            print("\n Opción inválida. Intenta de nuevo.\n")


def mostrar_info_sistema():
    """Muestra información del sistema y configuración"""
    print("\n" + "="*80)
    print("  INFORMACIÓN DEL SISTEMA")
    print("="*80 + "\n")
    
    from config_transformer import get_config
    import torch
    
    config = get_config('TRANSFORMER_CONFIG')
    
    print("  ARQUITECTURA DEL TRANSFORMER:")
    print(f"   • Dimensión del modelo: {config['d_model']}")
    print(f"   • Cabezas de atención: {config['num_heads']}")
    print(f"   • Capas transformer: {config['num_layers']}")
    print(f"   • Dimensión feed-forward: {config['d_ff']}")
    print(f"   • Longitud máxima: {config['max_len']}")
    print(f"   • Tamaño vocabulario: {config['vocab_size']}")
    
    print("\n  PARÁMETROS DE GENERACIÓN:")
    print(f"   • Temperature: {config['temperature']}")
    print(f"   • Top-K: {config['top_k']}")
    print(f"   • Longitud máxima generación: {config['max_generate_length']}")
    
    print("\n HARDWARE:")
    print(f"   • PyTorch: {torch.__version__}")
    print(f"   • CUDA disponible: {' Sí' if torch.cuda.is_available() else ' No'}")
    if torch.cuda.is_available():
        print(f"   • GPU: {torch.cuda.get_device_name(0)}")
    
    print("\n ARCHIVOS:")
    import os
    archivos = {
        'Modelo Transformer': 'models/transformer_chatbot.pth',
        'Datos de entrenamiento': 'data/chatbot_training_data.json',
        'Configuración': 'config_transformer.py'
    }
    
    for nombre, ruta in archivos.items():
        existe = "" if os.path.exists(ruta) else ""
        print(f"   {existe} {nombre}: {ruta}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n ¡Adiós!\n")
    except Exception as e:
        print(f"\n Error fatal: {e}\n")
        import traceback
        traceback.print_exc()

