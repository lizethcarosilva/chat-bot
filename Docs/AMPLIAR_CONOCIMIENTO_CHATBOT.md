#  CÓMO AMPLIAR EL CONOCIMIENTO DEL CHATBOT

##  PROBLEMA IDENTIFICADO

Tu chatbot tiene **2 fuentes de información:**

###  Bien cubierto:
- Datos de la BD (clientes, citas, estadísticas)

###  Limitado:
- Información veterinaria (enfermedades, cuidados, tratamientos)

---

##  SOLUCIÓN: Agregar Más Intenciones al JSON

---

##  PASO A PASO

### PASO 1: Abre el archivo

```
datos_veterinarios.json
```

### PASO 2: Busca el final del array "intents"

Busca la última intención antes del cierre `]`

### PASO 3: Agrega coma y nuevas intenciones

** IMPORTANTE:**
- Cada intención se separa con `,`
- La última intención NO lleva coma
- Mínimo 10 patterns por intención
- Responses detalladas y útiles

---

##  INTENCIONES NUEVAS PARA AGREGAR

### 1. ENFERMEDADES DE PIEL (Común)

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
    "piel seca y escamosa",
    "mi perro se rasca constantemente",
    "caída excesiva de pelo",
    "mi gato tiene calvas",
    "picazón en mascotas",
    "dermatitis atópica",
    "alergia alimentaria síntomas",
    "mi mascota tiene costras",
    "infección de piel"
  ],
  "responses": [
    " ENFERMEDADES DE PIEL EN MASCOTAS:\n\n DERMATITIS ALÉRGICA:\n• Síntomas: Picazón intensa, rascado excesivo, piel roja e inflamada, pérdida de pelo\n• Causas: Alergias alimentarias, pulgas, polen, ácaros del polvo\n• Tratamiento: Identificar y eliminar alérgeno, antihistamínicos, corticosteroides, champús medicados\n• Prevención: Dieta hipoalergénica, control de pulgas, limpieza regular\n\n INFECCIONES POR HONGOS (Dermatofitosis):\n• Síntomas: Áreas circulares sin pelo, escamas, costras, puede tener olor\n• Contagioso: SÍ (entre mascotas y humanos)\n• Tratamiento: Antifúngicos tópicos (cremas), antifúngicos orales en casos severos, aislamiento\n• Duración: 6-12 semanas de tratamiento\n\n SARNA:\n• Síntomas: Picazón severa (especialmente de noche), pérdida de pelo, costras gruesas, piel engrosada\n• Causas: Ácaros (Sarcoptes o Demodex)\n• Tratamiento: Medicamentos antiparasitarios (ivermectina, selamectina), baños medicados\n• Contagioso: Sí (sarna sarcóptica)\n\n DERMATITIS POR PULGAS:\n• Síntomas: Rascado en base de cola, abdomen, muslos; puntitos negros (heces de pulgas)\n• Tratamiento: Eliminar pulgas (pipetas, collares), antiinflamatorios, antibióticos si hay infección secundaria\n• Prevención: Control mensual de pulgas TODO el año\n\n SEÑALES DE EMERGENCIA:\n• Sangrado activo de la piel\n• Hinchazón facial súbita (puede ser anafilaxia)\n• Olor putrefacto (infección severa)\n• Piel muy caliente al tacto\n• Letargo o fiebre acompañante\n\n Consulta veterinario si:\n• Picazón dura más de 3 días\n• Hay pérdida significativa de pelo\n• Aparecen llagas abiertas\n• La mascota no puede dormir por rascarse"
  ]
},
```

### 2. CUIDADOS DENTALES (Muy Importante)

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
    "enfermedad periodontal",
    "gingivitis en mascotas",
    "mi mascota tiene encías rojas",
    "pérdida de dientes",
    "halitosis en perros",
    "sangrado de encías",
    "mi perro babea mucho",
    "dolor al comer",
    "inflamación de encías",
    "prevención dental"
  ],
  "responses": [
    " CUIDADO DENTAL COMPLETO:\n\n CEPILLADO DIARIO (Ideal):\n• Usa SOLO pasta dental para mascotas (las humanas son tóxicas)\n• Cepillo de dientes suave o dedal de goma\n• Movimientos circulares suaves en línea de encías\n• Enfócate en parte externa de dientes\n• 2-3 minutos por sesión\n\n CÓMO INTRODUCIR EL CEPILLADO:\nSemana 1: Solo deja que lama la pasta (sabor agradable)\nSemana 2: Frota dientes con dedo (sin cepillo)\nSemana 3: Usa cepillo solo unos segundos\nSemana 4: Cepillado completo\n• SIEMPRE recompensa después\n\n ALTERNATIVAS AL CEPILLADO:\n• Snacks dentales (ej: Dentastix, Greenies)\n• Juguetes masticables específicos\n• Huesos de nylon o goma dura\n• Agua dental (aditivo para agua de beber)\n• Geles o sprays dentales\n• Dieta dental (croquetas diseñadas para limpiar)\n\n LIMPIEZA PROFESIONAL:\n• Frecuencia: Cada 1-2 años (según veterinario)\n• Proceso: Bajo anestesia general\n• Incluye: Limpieza profunda, raspado de sarro, pulido, evaluación de encías\n• Costo aproximado: Variable según tamaño\n• Razas pequeñas: Necesitan limpiezas más frecuentes\n\n SEÑALES DE ALERTA - Acude al veterinario:\n• Mal aliento persistente (olor putrefacto)\n• Encías rojas, inflamadas o sangrantes\n• Sarro marrón/amarillo visible\n• Pérdida de apetito o dificultad para comer\n• Babeo excesivo\n• Pawing (tocarse la boca con pata)\n• Diente flojo o roto\n• Bulto en encías o debajo de ojo\n\n ENFERMEDAD PERIODONTAL:\nETAPA 1 (Gingivitis): Encías rojas, reversible con limpieza\nETAPA 2 (Leve): Inicio de pérdida ósea (25%)\nETAPA 3 (Moderada): Pérdida ósea 25-50%\nETAPA 4 (Severa): Pérdida ósea >50%, puede perder dientes\n\n DATO IMPORTANTE:\nEl 80% de perros y 70% de gatos mayores de 3 años tienen alguna forma de enfermedad dental. ¡La prevención es MÁS BARATA que el tratamiento!\n\n ALIMENTOS QUE AYUDAN:\n• Zanahorias crudas (pequeños trozos)\n• Manzana sin semillas\n• Apio\n• Calabaza\n• Evita: dulces, comida humana azucarada\n\n Prevenir enfermedad dental puede:\n• Agregar 2-5 años de vida\n• Evitar problemas cardíacos\n• Ahorrar miles en tratamientos"
  ]
},
```

### 3. NUTRICIÓN POR EDAD

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
    "porciones para cachorro",
    "cuándo cambiar de comida cachorro",
    "cachorro y leche",
    "destete cachorros",
    "alimentación gatitos",
    "nutrición primeros meses",
    "vitaminas para cachorros",
    "calcio para cachorros",
    "proteínas cachorro necesita",
    "mi cachorro está delgado",
    "cachorro con sobrepeso"
  ],
  "responses": [
    " NUTRICIÓN PARA CACHORROS (0-12 meses):\n\n TIPO DE ALIMENTO:\n• OBLIGATORIO: Alimento especial para cachorros (Puppy/Kitten)\n• Por qué: Mayor contenido proteico (min 25-30%)\n• Rico en: Calcio, fósforo, DHA (desarrollo cerebral), vitaminas\n• Tamaño croqueta: Pequeño (fácil de masticar)\n• NO usar: Alimento de adultos (insuficiente para crecimiento)\n\n⏰ FRECUENCIA DE COMIDAS:\n2-3 meses: 4 comidas al día\n  > Cada 4-5 horas\n  > Porciones pequeñas\n\n3-6 meses: 3 comidas al día\n  > Cada 6-7 horas\n  > Desayuno, almuerzo, cena\n\n6-12 meses: 2 comidas al día\n  > Cada 10-12 horas\n  > Mañana y tarde\n\n12+ meses: 2 comidas al día (continuar)\n  > Ya puede cambiar a alimento adulto\n\n CANTIDAD POR COMIDA:\n• Sigue ESTRICTAMENTE la tabla del empaque según peso actual\n• Divide la cantidad diaria entre número de comidas\n• Ejemplo: Si dice 200g al día y come 4 veces  50g por comida\n\n CONTROL DE PESO:\nDEMASIADO DELGADO:\n• Se ven costillas claramente\n• Cintura muy marcada\n• Solución: Aumenta 10% la porción\n\nPESO IDEAL:\n• Costillas se sienten al palpar pero no se ven\n• Cintura visible desde arriba\n• Abdomen recogido visto de lado\n\nSOBREPESO:\n• No se sienten costillas fácilmente\n• No hay cintura\n• Solución: Reduce 10% la porción\n\n HIDRATACIÓN:\n• Agua fresca SIEMPRE disponible\n• Cambiar 2-3 veces al día\n• Cachorros se deshidratan rápido\n\n ALIMENTOS PROHIBIDOS:\n• Chocolate (tóxico, puede ser mortal)\n• Cebolla y ajo (dañan glóbulos rojos)\n• Uvas y pasas (fallo renal)\n• Aguacate (persin es tóxico)\n• Huesos cocidos (se astillan)\n• Leche de vaca (causa diarrea)\n• Comida con mucha sal o grasa\n• Xilitol (endulzante, mortal)\n• Cafeína\n• Alcohol\n\n SNACKS PERMITIDOS (10% del total diario):\n• Zanahoria cruda pequeña\n• Trocitos de manzana (sin semillas)\n• Pollo cocido sin hueso ni piel\n• Calabaza cocida\n• Sandía sin semillas\n\n TRANSICIÓN DE ALIMENTO:\nCuándo: A los 12 meses (razas pequeñas) o 18-24 meses (razas grandes)\n\nCómo hacer el cambio (7 días):\nDía 1-2: 75% cachorro + 25% adulto\nDía 3-4: 50% cachorro + 50% adulto\nDía 5-6: 25% cachorro + 75% adulto\nDía 7: 100% adulto\n\n SEÑALES DE PROBLEMA NUTRICIONAL:\n• Diarrea persistente (más de 2 días)\n• Vómito frecuente\n• Pérdida de apetito por más de 1 comida\n• Pelo opaco o quebradizo\n• Piel seca con caspa\n• Bajo energía constante\n• Crecimiento muy lento\n• Abdomen muy distendido\n\n CONSEJO DE ORO:\nLa nutrición en los primeros 12 meses determina:\n• Salud ósea de por vida\n• Sistema inmune\n• Desarrollo cerebral\n• Longevidad\n\n¡Invierte en alimento de CALIDAD! Es más barato que tratamientos veterinarios futuros."
  ]
},
```

### 4. PRIMEROS AUXILIOS (ESENCIAL)

```json
{
  "tag": "primeros_auxilios",
  "patterns": [
    "primeros auxilios mascotas",
    "mi perro se cortó",
    "mi gato tiene una herida",
    "sangrado en mascota",
    "qué hacer si mi perro sangra",
    "heridas en mascotas",
    "mi mascota se golpeó",
    "accidente con mascota",
    "emergencia veterinaria",
    "botiquín para mascotas",
    "mi perro se quemó",
    "mi gato se envenenó",
    "atragantamiento en perros",
    "convulsiones en mascotas",
    "desmayo mascota",
    "trauma en mascota",
    "fractura en perro",
    "mordedura de perro",
    "picadura en mascota",
    "electrocución mascota"
  ],
  "responses": [
    " PRIMEROS AUXILIOS PARA MASCOTAS:\n\n REGLA DE ORO: Primeros auxilios NO sustituyen atención veterinaria. Son medidas TEMPORALES hasta llegar al veterinario.\n\n HERIDAS Y SANGRADO:\n\nSANGRADO LEVE:\n1. Lava con agua limpia o suero fisiológico\n2. Aplica presión directa con gasa limpia (2-3 min)\n3. Desinfecta con clorhexidina (NO alcohol ni agua oxigenada)\n4. Cubre con venda si es necesario\n5. Monitorea que no se infecte\n\nSANGRADO SEVERO:\n1. Mantén CALMA (tu mascota siente tu nerviosismo)\n2. Aplica presión FUERTE directa con toalla limpia\n3. NO quites la primera toalla (si se empapa, pon otra encima)\n4. Eleva la extremidad si es posible\n5. Ve INMEDIATAMENTE al veterinario\n6. Si sangrado no para en 5 min  EMERGENCIA\n\n QUEMADURAS:\n\n1. Aleja de la fuente de calor\n2. Enfría con agua fría (NO helada) por 10-15 min\n3. NO apliques: hielo, mantequilla, pasta dental\n4. Cubre con gasa húmeda limpia\n5. Ve al veterinario (las quemaduras se infectan fácilmente)\n\nQUEMADURA QUÍMICA:\n1. Enjuaga abundantemente con agua (15-20 min)\n2. NO intentes neutralizar\n3. Veterinario URGENTE\n\n FRACTURAS O TRAUMA:\n\n1. NO muevas a la mascota si sospechas lesión espinal\n2. Si debes moverla: usa tabla rígida o manta como camilla\n3. Inmoviliza extremidad fracturada si puedes (con cartón/toalla)\n4. NO intentes acomodar el hueso\n5. Transporte URGENTE al veterinario\n\n ELECTROCUCIÓN:\n\n1. NO toques a la mascota si aún está en contacto\n2. Desconecta electricidad PRIMERO\n3. Si no respira: RCP (abajo instrucciones)\n4. Veterinario URGENTE (daño interno puede ser severo)\n\n ENVENENAMIENTO:\n\n1. Identifica QUÉ consumió (lleva empaque/muestra)\n2. NO induzcas vómito (a menos que veterinario lo indique)\n3. Guarda muestra de vómito si hay\n4. Llama al veterinario INMEDIATAMENTE\n5. Lleva a emergencia (minutos cuentan)\n\nVENENOS COMUNES:\n• Chocolate, xilitol, anticongelante, raticida, insecticida\n\n ATRAGANTAMIENTO:\n\nMANIOBRA DE HEIMLICH:\n1. Verifica que realmente hay obstrucción (no puede respirar)\n2. Abre boca y ve si puedes sacar objeto con dedos\n3. SI NO:\n   - Perro pequeño: levanta por patas traseras, golpes secos en espalda\n   - Perro grande: abraza por detrás, presión rápida hacia arriba en abdomen\n4. 5 golpes en espalda, 5 compresiones abdominales\n5. Repite hasta expulsar o perder conciencia\n6. Si pierde conciencia  RCP\n\n RCP (Resucitación Cardiopulmonar):\n\nVERIFICA:\n1. ¿Respira? (mira pecho subir/bajar)\n2. ¿Tiene pulso? (parte interna muslo)\n\nSI NO RESPIRA NI TIENE PULSO:\n\n1. POSICIÓN: Acuesta de lado derecho en superficie firme\n\n2. COMPRESIONES:\n   • Perro pequeño/gato: Una mano sobre el corazón\n   • Perro grande: Ambas manos, brazos extendidos\n   • Ubicación: Detrás del codo, sobre corazón\n   • Ritmo: 100-120 compresiones por minuto\n   • Profundidad: 1/3 del ancho del pecho\n   • 30 compresiones\n\n3. RESPIRACIONES:\n   • Cierra hocico con mano\n   • Sopla en nariz (2 respiraciones)\n   • Ve que pecho se expanda\n   • 30 compresiones : 2 respiraciones\n\n4. CONTINÚA hasta:\n   • Mascota respira sola\n   • Llegas al veterinario\n   • 20 minutos sin respuesta\n\n BOTIQUÍN BÁSICO PARA MASCOTAS:\n\nMATERIAL:\n• Gasas estériles\n• Vendas autoadhesivas\n• Esparadrapo\n• Algodón\n• Suero fisiológico\n• Clorhexidina\n• Tijeras de punta roma\n• Pinzas\n• Termómetro digital rectal\n• Jeringa (sin aguja) para dar líquidos\n• Guantes desechables\n• Manta térmica\n\nMEDICAMENTOS (SOLO CON APROBACIÓN VETERINARIA):\n• Antihistamínico (para reacciones alérgicas)\n• Carbón activado (para envenenamientos)\n\nIMPORTANTE:\n• Teléfono del veterinario\n• Teléfono de emergencias 24h\n• Dirección de clínica más cercana\n\n CUÁNDO ES VERDADERA EMERGENCIA:\n• Dificultad para respirar\n• Sangrado que no para\n• Convulsiones\n• Pérdida de conciencia\n• Vómito o diarrea con sangre\n• Abdomen hinchado y duro\n• Trauma severo\n• Ingestión de tóxico\n• Temperatura >40°C o <37°C\n• Llanto constante de dolor\n\n EN EMERGENCIA:\n1. LLAMA al veterinario mientras vas en camino\n2. Avisa que vienes (se preparan)\n3. Maneja con cuidado pero RÁPIDO\n4. Que alguien más conduzca si es posible\n\n PREVENCIÓN:\n• Ten siempre a mano teléfono del vet\n• Ubica clínicas 24h cercanas\n• Toma curso de primeros auxilios (muchos vets los dan)\n• Botiquín accesible\n• Mantén calma en emergencias"
  ]
},
```

### 5. COMPORTAMIENTO CANINO

```json
{
  "tag": "comportamiento_perros",
  "patterns": [
    "mi perro ladra mucho",
    "perro destructivo",
    "ansiedad por separación",
    "mi perro muerde",
    "agresividad en perros",
    "perro hiperactivo",
    "cómo educar a mi perro",
    "entrenamiento canino",
    "mi perro no obedece",
    "perro ansioso",
    "perro que salta sobre la gente",
    "mi perro hace pis en casa",
    "perro que jala la correa",
    "socialización perros",
    "miedo en perros",
    "perro reactivo",
    "problemas de comportamiento",
    "adiestramiento básico",
    "mi perro llora cuando me voy",
    "perro territorial"
  ],
  "responses": [
    " GUÍA DE COMPORTAMIENTO CANINO:\n\n LADRIDO EXCESIVO:\n\nCAUSAS:\n• Aburrimiento (falta ejercicio/estimulación)\n• Soledad (ansiedad por separación)\n• Alerta (protección territorial)\n• Miedo o ansiedad\n• Buscar atención\n• Frustración\n\nSOLUCIONES:\n1. Ejercicio diario (mínimo 30-60 min según raza)\n2. Estimulación mental (juguetes interactivos, entrenamiento)\n3. Ignora ladridos de atención (NO recompenses con atención)\n4. Recompensa el silencio\n5. Identifica y elimina triggers\n6. Entrenamiento comando \"Silencio\"\n7. No dejes solo por períodos muy largos\n\n ANSIEDAD POR SEPARACIÓN:\n\nSÍNTOMAS:\n• Ladrido/llanto al dejarlo solo\n• Destrucción (puertas, ventanas)\n• Defecación/orinación en casa\n• Jadeo excesivo\n• Salivación\n• Intento de escape\n\nSOLUCIONES:\n1. Desensibilización gradual:\n   - Sal 5 segundos, vuelve\n   - Aumenta tiempo progresivamente\n   - No hagas drama al salir/entrar\n2. Crea espacio seguro (cama, juguetes favoritos)\n3. Deja ropa con tu olor\n4. Música relajante o TV prendida\n5. Ejercicio ANTES de salir\n6. Juguetes interactivos (Kong relleno)\n7. Evita saludos efusivos al volver\n8. Considera adoptar segunda mascota (compañía)\n9. En casos severos: Consulta etólogo, medicación ansiolítica\n\n MORDIDAS Y MASTICACIÓN:\n\nCACHORROS (Dentición):\n• Normal hasta 6-7 meses\n• Solución: Juguetes para morder (Kong, mordedores)\n• Redirige a juguete cada vez que muerda\n• Congela juguetes (alivia encías)\n\nADULTOS (Destructivo):\n1. Ejercicio diario suficiente\n2. Estimulación mental\n3. No dejar solo muchas horas\n4. Juguetes interactivos cuando solo\n5. Confina en área segura si es necesario\n6. NO castigues después del hecho (no entiende)\n\nAGRESIVIDAD POR BOCA:\n1. Grita \"¡AY!\" fuerte cuando muerda\n2. Detén juego inmediatamente\n3. Ignora 30 segundos\n4. NUNCA uses violencia\n5. Recompensa juego suave\n\n HIPERACTIVIDAD:\n\nDIFERENCIA:\n• Normal: Energético, se calma después de ejercicio\n• Hiperactivo: Siempre en movimiento, nunca se cansa, no se concentra\n\nMANEJO:\n1. Ejercicio intenso 2 veces al día\n2. Deportes caninos (agility, flyball)\n3. Entrenamiento de obediencia (enfoca energía)\n4. Establece rutinas claras\n5. Enseña comando \"Calmado\"\n6. Evita juegos que sobreexciten\n7. Dieta adecuada (sin exceso de proteína)\n8. Si es extremo: Consulta veterinario (puede ser hipertiroidismo)\n\n ENTRENAMIENTO BÁSICO (Comandos Esenciales):\n\n1. SENTADO:\n   • Sostén premio sobre nariz\n   • Mueve hacia atrás y arriba\n   • Trasero baja automáticamente\n   • Di \"Sentado\" + recompensa\n   • Practica 10 min diarios\n\n2. QUIETO:\n   • Comienza con \"Sentado\"\n   • Di \"Quieto\", da un paso atrás\n   • Si se mueve, vuelve a posición original\n   • Aumenta distancia gradualmente\n   • Recompensa después de liberar (\"Ya\")\n\n3. AQUÍ/VEN:\n   • NUNCA llames para castigar\n   • Usa voz alegre\n   • Agáchate, brazos abiertos\n   • Gran recompensa al venir\n   • Practica con correa larga primero\n\n4. JUNTO (No jalar correa):\n   • Detente cada vez que jale\n   • Solo avanza cuando afloje\n   • Recompensa caminar a tu lado\n   • Cambios de dirección frecuentes\n   • Paciencia (toma semanas)\n\n SOCIALIZACIÓN (CRÍTICA hasta 16 semanas):\n\nEXPONER A:\n• Diferentes personas (edades, apariencias)\n• Otros perros (vacunados)\n• Ambientes (parque, ciudad, carro)\n• Sonidos (tráfico, aspiradora, truenos)\n• Superficies (grass, cemento, metal)\n• Situaciones (veterinario, grooming)\n\nCÓMO:\n• Exposición POSITIVA (con premios)\n• Gradual, sin forzar\n• Observa lenguaje corporal\n• No sobreproteger\n• Clases de socialización puppy\n\n MIEDOS Y FOBIAS:\n\nCOMUNES:\n• Truenos/fuegos artificiales\n• Veterinario\n• Otros perros\n• Personas extrañas\n• Objetos (escoba, aspiradora)\n\nMANEJO:\n1. NO fuerces enfrentamiento\n2. NO consueles (refuerza miedo)\n3. Actúa normal, relajado\n4. Desensibilización gradual\n5. Contracondicionar (miedo + premio)\n6. Refugio seguro disponible\n7. Considera Thundershirt (presión calmante)\n8. En fobias severas: Medicación ansiolítica\n\n SEÑALES DE ESTRÉS:\n• Jadeo excesivo\n• Lamerse labios/nariz\n• Orejas hacia atrás\n• Cola entre patas\n• Evitar contacto visual\n• Pelo erizado\n• Postura agachada\n• Bostezos (en situación no tranquila)\n\n NUNCA:\n• Usar violencia física\n• Gritar constantemente\n• Restregar nariz en orina/heces\n• Usar collares de pinchos o eléctricos\n• Castigar después del hecho\n• Alpha rolls (voltear de espalda)\n\n PRINCIPIOS DE ENTRENAMIENTO:\n• Consistencia (todos en casa con mismas reglas)\n• Paciencia\n• Recompensa inmediata\n• Sesiones cortas (5-10 min)\n• Termina en positivo\n• Refuerzo positivo > castigo\n\n CUÁNDO BUSCAR PROFESIONAL:\n• Agresividad hacia personas/animales\n• Fobias severas\n• Ansiedad incontrolable\n• Problemas no mejoran en 4-6 semanas\n• Riesgo para seguridad\n\nBusca:\n• Etólogo veterinario (especialista comportamiento)\n• Adiestrador certificado (refuerzo positivo)\n• Evita \"entrenadores\" que usan dolor/miedo"
  ]
},
```

---

##  CÓMO AGREGAR AL ARCHIVO

### Ubicación exacta:

1. Abre `datos_veterinarios.json`
2. Busca el final del array (antes del último `]`)
3. Agrega una coma `,` después de la última intención existente
4. Pega las nuevas intenciones
5. La ÚLTIMA nueva intención NO lleva coma

### Ejemplo visual:

```json
{
  "intents": [
    {
      "tag": "existente_1",
      ...
    },
    {
      "tag": "existente_2",
      ...
    },   AGREGA COMA AQUÍ
    
     PEGA NUEVAS INTENCIONES AQUÍ
    
    {
      "tag": "enfermedades_piel",
      ...
    },
    {
      "tag": "cuidados_dentales",
      ...
    },
    {
      "tag": "nutricion_cachorros",
      ...
    }   SIN COMA EN LA ÚLTIMA
    
  ]
}
```

---

##  DESPUÉS DE AGREGAR

### PASO 1: Validar JSON

```bash
# Verifica que el JSON sea válido
python -m json.tool datos_veterinarios.json
```

Si hay error, muestra la línea con problema.

### PASO 2: Re-entrenar

```bash
python entrenar_chatbot_veterinario.py
```

Verás:
```
 Total de intenciones: 50  (antes eran 45)
 Total de patrones: 982  (antes eran 782)
```

### PASO 3: Reiniciar API

```bash
Ctrl+C
python api.py
```

### PASO 4: Probar

```
POST http://localhost:8000/api/chat

Body:
{
  "mensaje": "mi perro tiene la piel roja",
  "usuario_id": "test"
}
```

Debería responder con información detallada sobre enfermedades de piel. 

---

##  CONSEJOS PARA CREAR BUENAS INTENCIONES

### 1. Patterns (Entradas):
-  Mínimo 15-20 por intención
-  Incluye variaciones (formal, informal)
-  Con y sin signos de puntuación
-  Singular y plural
-  Diferentes formas de preguntar lo mismo

### 2. Responses (Respuestas):
-  Detalladas y útiles
-  Estructura clara (usa emojis, saltos de línea)
-  Información precisa
-  Incluye advertencias cuando necesario
-  Sugiere cuándo consultar veterinario

### 3. Tags (Etiquetas):
-  Descriptivos
-  Snake_case (minúsculas_con_guión_bajo)
-  Únicos (no repetir)

---

##  MÁS TEMAS QUE PUEDES AGREGAR

### Enfermedades Específicas:
- Problemas respiratorios
- Problemas digestivos
- Problemas oculares
- Problemas de oído
- Problemas urinarios
- Artritis y dolor articular
- Diabetes en mascotas
- Problemas cardíacos

### Cuidados:
- Cuidado de uñas
- Baño y grooming
- Cuidado de orejas
- Ejercicio por raza
- Cuidado en invierno/verano
- Viajes con mascotas
- Introducción de nueva mascota

### Reproducción:
- Esterilización/castración
- Embarazo en mascotas
- Parto
- Cuidado de cachorros recién nacidos

### Por Etapa de Vida:
- Cuidado de senior (7+ años)
- Transición cachorro-adulto
- Cuidados paliativos

---

##  GUÍA RÁPIDA

**Para ampliar conocimiento:**
1. Abre `datos_veterinarios.json`
2. Copia-pega nuevas intenciones (arriba hay 5 completas)
3. Valida JSON
4. Re-entrena: `python entrenar_chatbot_veterinario.py`
5. Reinicia API
6. Prueba preguntas nuevas

**Cada intención nueva:**
- 15-20 patterns mínimo
- Responses detalladas
- Información precisa y útil

---

##  PARA TU EXPOSICIÓN

**Explica:**

*"El chatbot combina 2 fuentes de información:*

*1. **Base de datos:** Para consultas de negocio (clientes, citas, análisis)*

*2. **Conocimiento entrenado:** Para información veterinaria general*

*El archivo `datos_veterinarios.json` contiene 50+ intenciones con 1000+ ejemplos de preguntas. Al entrenar con LSTM, el modelo aprende a:*
- *Entender sinónimos*
- *Reconocer variaciones en preguntas*
- *Generalizar a preguntas no vistas*

*Por ejemplo, si entrenamos con \"mi perro tiene la piel roja\", también entenderá \"mi mascota tiene dermatitis\" o \"problemas cutáneos en mi can\"."*

---

##  RESUMEN

**Problema:** Chatbot limitado en información veterinaria

**Solución:** Ampliar `datos_veterinarios.json` con más intenciones

**Proceso:**
1. Agregar intenciones con patterns y responses
2. Re-entrenar modelo LSTM
3. Chatbot ahora entiende más temas

**Resultado:** Chatbot más completo y útil 

---

**¿Quieres que te ayude a agregar algún tema específico que te interese?** 

