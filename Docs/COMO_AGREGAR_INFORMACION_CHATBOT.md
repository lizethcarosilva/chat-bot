#  CÓMO AGREGAR INFORMACIÓN AL CHATBOT

##  ¿Quieres que el chatbot sepa sobre enfermedades y cuidados?

Hay **2 formas** de agregar información:

---

##  FORMA 1: Agregar al archivo JSON (Para entrenar LSTM)

### PASO 1: Abrir el archivo de datos

```
datos_veterinarios.json
```

### PASO 2: Agregar nueva intención

**Formato:**
```json
{
  "tag": "nombre_de_la_intencion",
  "patterns": [
    "ejemplo de pregunta 1",
    "ejemplo de pregunta 2",
    "ejemplo de pregunta 3",
    "mínimo 10 ejemplos diferentes"
  ],
  "responses": [
    "Respuesta detallada 1",
    "Respuesta alternativa 2",
    "Respuesta variante 3"
  ]
}
```

### PASO 3: Ejemplos Reales para Agregar

#### Ejemplo 1: Enfermedades de Piel

Agrega esto al archivo `datos_veterinarios.json`:

```json
{
  "tag": "enfermedades_piel",
  "patterns": [
    "mi perro tiene problemas de piel",
    "enfermedades de piel en mascotas",
    "mi gato tiene la piel roja",
    "dermatitis en perros",
    "alergia en la piel",
    "mi mascota se rasca mucho",
    "piel irritada",
    "problemas dermatológicos",
    "sarpullido en perro",
    "eccema en gatos",
    "hongos en la piel",
    "piel seca y escamosa"
  ],
  "responses": [
    "Las enfermedades de piel más comunes en mascotas incluyen:\n\n DERMATITIS ALÉRGICA:\n• Síntomas: Picazón intensa, rascado, piel roja\n• Causas: Alergias alimentarias, pulgas, polen\n• Tratamiento: Identificar alérgeno, medicación antihistamínica\n\n HONGOS (Dermatofitosis):\n• Síntomas: Áreas circulares sin pelo, escamas\n• Contagioso: Sí (entre mascotas y humanos)\n• Tratamiento: Antifúngicos tópicos u orales\n\n SARNA:\n• Síntomas: Picazón severa, pérdida de pelo, costras\n• Causas: Ácaros\n• Tratamiento: Medicamentos antiparasitarios\n\n IMPORTANTE: Si la piel está muy inflamada, con sangrado o mal olor, consulta veterinario inmediatamente."
  ]
}
```

#### Ejemplo 2: Cuidados Dentales

```json
{
  "tag": "cuidados_dentales",
  "patterns": [
    "cuidado dental en mascotas",
    "cómo cepillar dientes de perro",
    "mi perro tiene mal aliento",
    "higiene dental mascotas",
    "limpieza dental",
    "caries en perros",
    "sarro en dientes",
    "dientes amarillos perro",
    "cepillado dental gatos",
    "problemas dentales",
    "enfermedad periodontal"
  ],
  "responses": [
    "El cuidado dental es crucial para la salud de tu mascota:\n\n CEPILLADO DIARIO:\n• Usa pasta dental para mascotas (nunca humana)\n• Cepillo de dientes suave especial para mascotas\n• Introduce gradualmente (1-2 semanas)\n• Recompensa después del cepillado\n\n ALTERNATIVAS:\n• Snacks dentales (galletas especiales)\n• Juguetes masticables\n• Agua dental (aditivo para agua de beber)\n\n LIMPIEZA PROFESIONAL:\n• Anual o cada 2 años\n• Bajo anestesia\n• Remueve sarro y placa\n\n SEÑALES DE ALERTA:\n• Mal aliento persistente\n• Encías rojas o sangrantes\n• Pérdida de apetito\n• Babeo excesivo\n\n Prevenir es más fácil que tratar. El 80% de perros mayores de 3 años tienen alguna enfermedad dental."
  ]
}
```

#### Ejemplo 3: Nutrición Específica

```json
{
  "tag": "nutricion_cachorros",
  "patterns": [
    "alimentación para cachorros",
    "qué darle de comer a un cachorro",
    "nutrición cachorros",
    "comida para perros bebés",
    "cuánto come un cachorro",
    "frecuencia alimentación cachorro",
    "mejor alimento para cachorros",
    "cachorro no quiere comer",
    "dieta cachorro",
    "porciones para cachorro"
  ],
  "responses": [
    "Nutrición para CACHORROS (0-12 meses):\n\n TIPO DE ALIMENTO:\n• Alimento especial para cachorros (puppy/kitten)\n• Alto en proteínas (min 25-30%)\n• Rico en calcio y DHA\n• Tamaño de croqueta pequeño\n\n⏰ FRECUENCIA:\n• 2-3 meses: 4 comidas al día\n• 3-6 meses: 3 comidas al día\n• 6-12 meses: 2 comidas al día\n\n PORCIONES:\n• Sigue tabla del empaque según peso\n• Ajusta si engorda o adelgaza\n• Agua fresca siempre disponible\n\n NUNCA DES:\n• Comida de adultos (bajo en nutrientes)\n• Huesos cocidos (se astillan)\n• Chocolate, cebolla, ajo\n• Leche (causa diarrea)\n\n La nutrición en cachorros determina su salud futura. ¡Invierte en alimento de calidad!"
  ]
}
```

---

##  PASO 4: Dónde Agregar en el Archivo

Abre `datos_veterinarios.json` y busca la estructura:

```json
{
  "intents": [
    {
      "tag": "saludo",
      ...
    },
    {
      "tag": "despedida",
      ...
    },
    
     AQUÍ AGREGAS TUS NUEVAS INTENCIONES
    
    {
      "tag": "enfermedades_piel",
      "patterns": [...],
      "responses": [...]
    },
    {
      "tag": "cuidados_dentales",
      "patterns": [...],
      "responses": [...]
    }
    
  ]
}
```

** IMPORTANTE:**
- Cada intención debe estar separada por coma `,`
- La última intención NO lleva coma
- Verifica que el JSON sea válido

---

##  FORMA 2: Agregar Respuestas Directas (Sin entrenar)

Si NO quieres entrenar, agrega directamente en `chatbot.py`:

### PASO 1: Agregar método de respuesta

```python
def responder_enfermedades_piel(self) -> str:
    """Responde sobre enfermedades de piel"""
    return """
 ENFERMEDADES DE PIEL EN MASCOTAS

DERMATITIS ALÉRGICA:
• Síntomas: Picazón intensa, rascado, piel roja
• Causas: Alergias alimentarias, pulgas, polen
• Tratamiento: Identificar alérgeno, antihistamínicos

HONGOS:
• Síntomas: Áreas sin pelo, escamas
• Contagioso: Sí
• Tratamiento: Antifúngicos

SARNA:
• Síntomas: Picazón severa, costras
• Causa: Ácaros
• Tratamiento: Antiparasitarios

 Consulta veterinario si hay inflamación severa.
"""
```

### PASO 2: Agregar detección

En `detectar_intencion()`:

```python
# Enfermedades de piel
if any(palabra in texto_norm for palabra in ['piel', 'dermatitis', 'sarpullido', 'rasca', 'hongos']):
    return 'enfermedades_piel'
```

### PASO 3: Conectar en procesar_mensaje

```python
elif intencion == 'enfermedades_piel':
    respuesta = self.responder_enfermedades_piel()
```

---

##  ¿CUÁL FORMA USAR?

### Usa FORMA 1 (JSON + Entrenar) si:
-  Quieres que el chatbot use IA
-  Tienes muchas intenciones (10+)
-  Quieres que entienda sinónimos

### Usa FORMA 2 (Código directo) si:
-  Solo necesitas pocas respuestas
-  Quieres control total del texto
-  No quieres entrenar

---

##  EJEMPLOS DE INTENCIONES QUE PUEDES AGREGAR

### Enfermedades:

1. **Enfermedades Respiratorias**
   - Patterns: "mi perro tose", "tos en gatos", "dificultad respirar"
   - Info: Tos de las perreras, neumonía, asma felino

2. **Problemas Digestivos**
   - Patterns: "vómito", "diarrea", "estreñimiento"
   - Info: Causas, tratamiento, cuándo es urgente

3. **Problemas Oculares**
   - Patterns: "ojos rojos", "conjuntivitis", "secreción ocular"
   - Info: Infecciones, alergias, cuerpos extraños

### Cuidados:

4. **Cuidado de Uñas**
   - Patterns: "cortar uñas", "cuidado de garras"
   - Info: Frecuencia, técnica, qué evitar

5. **Ejercicio por Raza**
   - Patterns: "cuánto ejercicio", "paseos necesarios"
   - Info: Según raza, edad, tamaño

6. **Primeros Auxilios**
   - Patterns: "mi perro se cortó", "heridas", "sangrado"
   - Info: Qué hacer, cuándo acudir al vet

---

##  PLANTILLA PARA AGREGAR

Copia y pega esto en `datos_veterinarios.json`:

```json
{
  "tag": "TU_INTENCION_AQUI",
  "patterns": [
    "pregunta 1",
    "pregunta 2",
    "pregunta 3",
    "pregunta 4",
    "pregunta 5",
    "pregunta 6",
    "pregunta 7",
    "pregunta 8",
    "pregunta 9",
    "pregunta 10"
  ],
  "responses": [
    "Tu respuesta detallada aquí.\n\nPuedes usar:\n• Viñetas\n• Saltos de línea\n• Emojis\n\n Advertencias importantes."
  ]
}
```

**Reglas:**
-  Mínimo 10 patterns por intención
-  Patterns variados (diferentes formas de preguntar)
-  Responses informativas y útiles
-  Usar formato markdown (\n para saltos de línea)

---

##  DESPUÉS DE AGREGAR INFORMACIÓN

### SI agregaste al JSON:

```bash
# 1. Guarda el archivo datos_veterinarios.json
# 2. Re-entrena el modelo
python entrenar_chatbot_veterinario.py
# 3. Reinicia la API
python api.py
```

### SI agregaste al código (chatbot.py):

```bash
# 1. Guarda chatbot.py
# 2. Reinicia la API
Ctrl+C
python api.py
```

---

##  AHORA: Soluciona el Error y Prueba de Nuevo

He arreglado el error del entrenamiento. **Reinicia la API** e intenta entrenar de nuevo:

```bash
# 1. Detén la API
Ctrl+C

# 2. Reinicia
python api.py

# 3. Entrena de nuevo
http://localhost:8000/docs  POST /api/entrenar  Execute
```

**Ahora debería funcionar sin error.** 

---

##  RESUMEN

**Error arreglado:**  El entrenamiento ahora maneja clases con pocos ejemplos

**Agregar información:**
- **Opción 1:** Edita `datos_veterinarios.json` y re-entrena
- **Opción 2:** Agrega métodos en `chatbot.py` directamente

**Temas que puedes agregar:**
- Enfermedades específicas (piel, respiratorias, digestivas)
- Cuidados especializados (dental, uñas, baño)
- Nutrición por edad/raza
- Primeros auxilios
- Comportamiento canino/felino

---

**¿Quieres que te ayude a agregar algún tema específico al chatbot?** 

