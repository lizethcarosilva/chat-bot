"""
MÓDULO DE ANÁLISIS PREDICTIVO CON REDES NEURONALES
Predice patrones y tendencias en los datos del Pet Store
"""

import numpy as np
import pandas as pd
import pickle
import logging
from typing import Dict, Tuple, List
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, silhouette_score
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding
from config import PREDICTOR_CONFIG, PATHS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PetStorePredictor:
    """
    Modelos de redes neuronales para análisis predictivo
    
    Predicciones:
    1. Tipo de mascota más común por servicio y hora
    2. Probabilidad de asistencia a citas
    3. Día con mayor demanda
    4. Recomendación de servicios
    """
    
    def __init__(self):
        self.model_tipo_mascota = None
        self.model_asistencia = None
        self.model_demanda = None
        
        self.label_encoder_tipo = LabelEncoder()
        self.label_encoder_servicio = LabelEncoder()
        self.scaler = StandardScaler()
        
        self.trained = False
    
    # =========================================================================
    # PREPARACIÓN DE DATOS
    # =========================================================================
    
    def preparar_datos_tipo_mascota(self, df: pd.DataFrame) -> Tuple:
        """
        Prepara datos para predecir el tipo de mascota más común
        Features: día_semana, hora, mes, service_id
        Target: tipo_mascota
        """
        logger.info("📊 Preparando datos para predicción de tipo de mascota...")
        
        # Eliminar registros nulos
        df_clean = df.dropna(subset=['tipo_mascota', 'dia_semana', 'hora', 'mes', 'service_id'])
        
        if len(df_clean) == 0:
            logger.error("❌ No hay datos suficientes para entrenar")
            return None, None, None, None
        
        # Features
        X = df_clean[['dia_semana', 'hora', 'mes', 'service_id']].values
        
        # Target
        y = self.label_encoder_tipo.fit_transform(df_clean['tipo_mascota'])
        
        # Dividir datos
        # Verificar si podemos hacer stratify (requiere al menos 2 ejemplos por clase)
        from collections import Counter
        class_counts = Counter(y)
        min_class_count = min(class_counts.values())
        
        # Solo usar stratify si todas las clases tienen al menos 2 ejemplos
        if min_class_count >= 2:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=PREDICTOR_CONFIG['test_size'],
                random_state=PREDICTOR_CONFIG['random_state'],
                stratify=y  # Mantiene proporción de clases
            )
        else:
            # Sin stratify si hay clases con pocos ejemplos
            logger.warning(f"⚠️ Algunas clases tienen pocos ejemplos ({min_class_count}). Entrenando sin stratify.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=PREDICTOR_CONFIG['test_size'],
                random_state=PREDICTOR_CONFIG['random_state']
            )
        
        # Escalar features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        # Convertir a categorical
        y_train_cat = keras.utils.to_categorical(y_train)
        y_test_cat = keras.utils.to_categorical(y_test)
        
        logger.info(f"✓ Datos preparados: {X_train.shape[0]} train, {X_test.shape[0]} test")
        logger.info(f"✓ Clases: {len(self.label_encoder_tipo.classes_)}")
        
        return X_train, X_test, y_train_cat, y_test_cat
    
    def preparar_datos_asistencia(self, df: pd.DataFrame) -> Tuple:
        """
        Prepara datos para predecir si un cliente asistirá a una cita
        Features: día_semana, hora, mes, service_id, edad_mascota
        Target: asistio (1=sí, 0=no)
        """
        logger.info("📊 Preparando datos para predicción de asistencia...")
        
        # Eliminar registros nulos
        df_clean = df.dropna(subset=['asistio', 'dia_semana', 'hora', 'mes', 
                                      'service_id', 'edad_mascota'])
        
        if len(df_clean) == 0:
            logger.error("❌ No hay datos suficientes para entrenar")
            return None, None, None, None
        
        # Features
        X = df_clean[['dia_semana', 'hora', 'mes', 'service_id', 'edad_mascota']].values
        
        # Target (binario)
        y = df_clean['asistio'].values
        
        # Dividir datos
        # Verificar balance de clases para stratify
        from collections import Counter
        class_counts = Counter(y)
        min_class_count = min(class_counts.values())
        
        if min_class_count >= 2:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=PREDICTOR_CONFIG['test_size'],
                random_state=PREDICTOR_CONFIG['random_state'],
                stratify=y
            )
        else:
            logger.warning(f"⚠️ Clases desbalanceadas ({min_class_count}). Entrenando sin stratify.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=PREDICTOR_CONFIG['test_size'],
                random_state=PREDICTOR_CONFIG['random_state']
            )
        
        # Escalar features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        logger.info(f"✓ Datos preparados: {X_train.shape[0]} train, {X_test.shape[0]} test")
        
        return X_train, X_test, y_train, y_test
    
    # =========================================================================
    # CONSTRUCCIÓN DE MODELOS
    # =========================================================================
    
    def construir_modelo_tipo_mascota(self, num_features: int, num_classes: int):
        """
        Red neuronal para clasificar tipo de mascota
        Arquitectura: Dense → Dropout → Dense → Softmax
        """
        logger.info("🏗️  Construyendo modelo de predicción de tipo de mascota...")
        
        model = Sequential([
            Dense(128, activation='relu', input_shape=(num_features,)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("✓ Modelo construido")
        return model
    
    def construir_modelo_asistencia(self, num_features: int):
        """
        Red neuronal para predecir asistencia (clasificación binaria)
        Arquitectura: Dense → Dropout → Dense → Sigmoid
        """
        logger.info("🏗️  Construyendo modelo de predicción de asistencia...")
        
        model = Sequential([
            Dense(64, activation='relu', input_shape=(num_features,)),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )
        
        logger.info("✓ Modelo construido")
        return model
    
    # =========================================================================
    # ENTRENAMIENTO
    # =========================================================================
    
    def entrenar_modelo_tipo_mascota(self, df: pd.DataFrame) -> Dict:
        """Entrena el modelo de predicción de tipo de mascota"""
        logger.info("\n" + "=" * 80)
        logger.info("🚀 ENTRENANDO MODELO: Tipo de Mascota")
        logger.info("=" * 80)
        
        # Preparar datos
        X_train, X_test, y_train, y_test = self.preparar_datos_tipo_mascota(df)
        
        if X_train is None:
            return {"error": "Datos insuficientes"}
        
        # Construir modelo
        num_classes = y_train.shape[1]
        self.model_tipo_mascota = self.construir_modelo_tipo_mascota(
            X_train.shape[1], 
            num_classes
        )
        
        # Callbacks
        early_stop = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5
        )
        
        # Entrenar
        logger.info("\n📈 Entrenando...")
        history = self.model_tipo_mascota.fit(
            X_train, y_train,
            epochs=PREDICTOR_CONFIG['prediction_epochs'],
            batch_size=PREDICTOR_CONFIG['prediction_batch_size'],
            validation_split=0.2,
            callbacks=[early_stop, reduce_lr],
            verbose=1
        )
        
        # Evaluar
        logger.info("\n📊 Evaluando modelo...")
        y_pred = self.model_tipo_mascota.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1)
        
        accuracy = accuracy_score(y_test_classes, y_pred_classes)
        logger.info(f"✓ Precisión en test: {accuracy:.2%}")
        
        return {
            "accuracy": accuracy,
            "history": history.history,
            "classes": self.label_encoder_tipo.classes_.tolist()
        }
    
    def entrenar_modelo_asistencia(self, df: pd.DataFrame) -> Dict:
        """Entrena el modelo de predicción de asistencia"""
        logger.info("\n" + "=" * 80)
        logger.info("🚀 ENTRENANDO MODELO: Predicción de Asistencia")
        logger.info("=" * 80)
        
        # Preparar datos
        X_train, X_test, y_train, y_test = self.preparar_datos_asistencia(df)
        
        if X_train is None:
            return {"error": "Datos insuficientes"}
        
        # Construir modelo
        self.model_asistencia = self.construir_modelo_asistencia(X_train.shape[1])
        
        # Callbacks
        early_stop = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Entrenar
        logger.info("\n📈 Entrenando...")
        history = self.model_asistencia.fit(
            X_train, y_train,
            epochs=PREDICTOR_CONFIG['prediction_epochs'],
            batch_size=PREDICTOR_CONFIG['prediction_batch_size'],
            validation_split=0.2,
            callbacks=[early_stop],
            verbose=1
        )
        
        # Evaluar
        logger.info("\n📊 Evaluando modelo...")
        y_pred = (self.model_asistencia.predict(X_test) > 0.5).astype(int)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"✓ Precisión en test: {accuracy:.2%}")
        
        return {
            "accuracy": accuracy,
            "history": history.history
        }
    
    # =========================================================================
    # PREDICCIONES
    # =========================================================================
    
    def predecir_tipo_mascota(self, dia_semana: int, hora: int, 
                             mes: int, service_id: int) -> Dict:
        """
        Predice el tipo de mascota más probable para una cita
        
        Args:
            dia_semana: 0=Domingo, 1=Lunes, ..., 6=Sábado
            hora: 0-23
            mes: 1-12
            service_id: ID del servicio
        """
        if self.model_tipo_mascota is None:
            return {"error": "Modelo no entrenado"}
        
        # Preparar features
        X = np.array([[dia_semana, hora, mes, service_id]])
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        pred = self.model_tipo_mascota.predict(X_scaled, verbose=0)[0]
        
        # Obtener top 3 predicciones
        top_indices = np.argsort(pred)[-3:][::-1]
        
        predicciones = []
        for idx in top_indices:
            predicciones.append({
                "tipo_mascota": self.label_encoder_tipo.classes_[idx],
                "probabilidad": float(pred[idx])
            })
        
        return {
            "predicciones": predicciones,
            "tipo_mas_probable": predicciones[0]["tipo_mascota"],
            "confianza": predicciones[0]["probabilidad"]
        }
    
    def predecir_asistencia(self, dia_semana: int, hora: int, mes: int,
                           service_id: int, edad_mascota: int) -> Dict:
        """
        Predice la probabilidad de que un cliente asista a una cita
        
        Returns:
            Dict con probabilidad de asistencia
        """
        if self.model_asistencia is None:
            return {"error": "Modelo no entrenado"}
        
        # Preparar features
        X = np.array([[dia_semana, hora, mes, service_id, edad_mascota]])
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        probabilidad = float(self.model_asistencia.predict(X_scaled, verbose=0)[0][0])
        
        return {
            "probabilidad_asistencia": probabilidad,
            "asistira": probabilidad > 0.5,
            "confianza": "Alta" if probabilidad > 0.7 or probabilidad < 0.3 else "Media"
        }
    
    # =========================================================================
    # ANÁLISIS Y ESTADÍSTICAS
    # =========================================================================
    
    def analizar_tipo_mascota_mas_comun(self, df: pd.DataFrame) -> Dict:
        """Analiza qué tipo de mascota es más común"""
        tipo_counts = df['tipo_mascota'].value_counts()
        total = len(df)
        
        resultados = []
        for tipo, count in tipo_counts.items():
            resultados.append({
                "tipo": str(tipo),
                "cantidad": int(count),
                "porcentaje": round(count / total * 100, 2)
            })
        
        return {
            "tipo_mas_comun": resultados[0]["tipo"],
            "estadisticas": resultados
        }
    
    def analizar_dia_mas_atencion(self, df: pd.DataFrame) -> Dict:
        """Analiza qué día tiene más atención"""
        dias_nombre = {
            0: "Domingo", 1: "Lunes", 2: "Martes", 3: "Miércoles",
            4: "Jueves", 5: "Viernes", 6: "Sábado"
        }
        
        dia_counts = df['dia_semana'].value_counts().sort_index()
        
        resultados = []
        for dia, count in dia_counts.items():
            resultados.append({
                "dia": dias_nombre.get(int(dia), str(dia)),
                "numero_dia": int(dia),
                "cantidad_citas": int(count)
            })
        
        # Ordenar por cantidad
        resultados_ordenados = sorted(resultados, key=lambda x: x['cantidad_citas'], reverse=True)
        
        return {
            "dia_con_mas_atencion": resultados_ordenados[0]["dia"],
            "estadisticas": resultados_ordenados
        }
    
    def analizar_hora_pico(self, df: pd.DataFrame) -> Dict:
        """Analiza la hora con más demanda"""
        hora_counts = df['hora'].value_counts().sort_index()
        
        resultados = []
        for hora, count in hora_counts.items():
            resultados.append({
                "hora": int(hora),
                "cantidad_citas": int(count)
            })
        
        # Ordenar por cantidad
        resultados_ordenados = sorted(resultados, key=lambda x: x['cantidad_citas'], reverse=True)
        
        return {
            "hora_pico": resultados_ordenados[0]["hora"],
            "estadisticas": resultados_ordenados[:5]  # Top 5
        }
    
    # =========================================================================
    # HIERARCHICAL CLUSTERING
    # =========================================================================
    
    def clustering_mascotas(self, df: pd.DataFrame, n_clusters: int = 3) -> Dict:
        """
        HIERARCHICAL CLUSTERING DE MASCOTAS
        
        ¿Qué hace?
        - Agrupa mascotas con características similares
        - Usa Agglomerative Clustering (jerárquico ascendente)
        - Identifica patrones sin etiquetas previas
        
        ¿Cómo funciona?
        1. Selecciona features: edad, servicio, precio
        2. Estandariza datos (StandardScaler)
        3. Aplica algoritmo Agglomerative
        4. Evalúa calidad (Silhouette Score)
        5. Caracteriza cada cluster encontrado
        
        Args:
            df: DataFrame con datos de citas y mascotas
            n_clusters: Número de grupos a generar (default: 3)
            
        Returns:
            Dict con:
            - clusters: Lista de clusters con características
            - silhouette_score: Métrica de calidad (0-1)
            - linkage_matrix: Para dendrograma
        
        Ejemplo de uso:
            resultado = predictor.clustering_mascotas(df, n_clusters=3)
            print(resultado['clusters'][0]['tipo_mascota_predominante'])
        """
        logger.info(f"🔬 Aplicando Hierarchical Clustering a mascotas ({n_clusters} clusters)...")
        
        try:
            # PASO 1: PREPARAR DATOS
            # =====================
            # Seleccionamos solo las columnas relevantes para agrupar mascotas
            # Features = Características que definen la similitud entre mascotas
            df_clustering = df[['edad_mascota', 'service_id', 'precio_servicio']].copy()
            df_clustering = df_clustering.dropna()  # Eliminar datos faltantes
            
            # Validar que hay suficientes datos
            if len(df_clustering) < n_clusters:
                return {"error": "Datos insuficientes para clustering"}
            
            # PASO 2: ESTANDARIZACIÓN
            # =======================
            # StandardScaler normaliza los datos para que todos estén en la misma escala
            # Fórmula: z = (x - media) / desviación_estándar
            # Ejemplo: Edad (años) y Precio ($) tienen diferentes rangos
            #          Edad: 1-15, Precio: 10-500
            #          Después de escalar: ambos entre -2 y +2
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_clustering)
            
            # PASO 3: APLICAR CLUSTERING JERÁRQUICO
            # ======================================
            # AgglomerativeClustering = Algoritmo bottom-up (de abajo hacia arriba)
            # - Empieza con cada punto como un cluster individual
            # - Une clusters cercanos iterativamente
            # - Continúa hasta tener n_clusters grupos
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,    # Número de grupos finales
                linkage='ward',           # Método Ward: minimiza varianza intra-cluster
                metric='euclidean'        # Distancia euclidiana entre puntos
            )
            
            # fit_predict: Entrena el modelo y asigna etiquetas
            # Retorna array: [0, 0, 1, 2, 0, 1, ...] (cluster de cada mascota)
            labels = clustering.fit_predict(X_scaled)
            
            # PASO 4: EVALUAR CALIDAD
            # =======================
            # Silhouette Score: Mide qué tan bien están los clusters
            # -1 = Mal agrupados, 0 = Solapados, +1 = Bien separados
            silhouette_avg = silhouette_score(X_scaled, labels)
            
            # Agregar cluster a dataframe original
            df_clustering['cluster'] = labels
            
            # Analizar cada cluster
            clusters_info = []
            for i in range(n_clusters):
                cluster_data = df_clustering[df_clustering['cluster'] == i]
                
                # Obtener mascotas en este cluster
                mascotas_cluster = df[df_clustering['cluster'] == i]['tipo_mascota'].value_counts()
                
                clusters_info.append({
                    "cluster_id": int(i),
                    "total_mascotas": len(cluster_data),
                    "edad_promedio": float(cluster_data['edad_mascota'].mean()),
                    "precio_promedio": float(cluster_data['precio_servicio'].mean()),
                    "tipo_mascota_predominante": mascotas_cluster.index[0] if len(mascotas_cluster) > 0 else "N/A",
                    "distribucion_tipos": mascotas_cluster.to_dict()
                })
            
            # Calcular linkage para dendrograma
            Z = linkage(X_scaled, method='ward')
            
            logger.info(f"✓ Clustering completado. Silhouette Score: {silhouette_avg:.3f}")
            
            return {
                "n_clusters": n_clusters,
                "total_mascotas": len(df_clustering),
                "silhouette_score": float(silhouette_avg),
                "clusters": clusters_info,
                "linkage_matrix": Z.tolist(),
                "metodo": "Agglomerative (Ward)",
                "metrica": "Euclidean"
            }
            
        except Exception as e:
            logger.error(f"❌ Error en clustering: {e}")
            return {"error": str(e)}
    
    def clustering_clientes(self, df: pd.DataFrame, n_clusters: int = 4) -> Dict:
        """
        SEGMENTACIÓN DE CLIENTES CON HIERARCHICAL CLUSTERING
        
        ¿Para qué sirve?
        - Divide clientes en grupos homogéneos (VIP, Regular, Ocasional, Nuevo)
        - Permite marketing dirigido por segmento
        - Identifica clientes de alto valor automáticamente
        
        ¿Cómo funciona?
        1. Agrega datos por cliente (frecuencia, gasto, asistencia)
        2. Normaliza features con StandardScaler
        3. Aplica Agglomerative Clustering (método Average)
        4. Caracteriza cada segmento encontrado
        5. Ordena por valor económico
        
        Features utilizados:
        - total_citas: Cuántas veces ha visitado el cliente
        - gasto_total: Suma de todos los servicios contratados
        - tasa_asistencia: % de citas a las que asistió (0-1)
        
        Args:
            df: DataFrame con datos de citas y clientes
            n_clusters: Número de segmentos (default: 4)
                       Recomendado: 4 (VIP, Regular, Ocasional, Nuevo)
            
        Returns:
            Dict con:
            - segmentos: Lista con perfil de cada segmento
            - silhouette_score: Calidad del clustering
            - calidad_clustering: "Buena", "Moderada" o "Baja"
        
        Aplicaciones:
        - Marketing dirigido por segmento
        - Programas de lealtad para VIPs
        - Campañas de reactivación para ocasionales
        """
        logger.info(f"🔬 Segmentando clientes con Hierarchical Clustering ({n_clusters} grupos)...")
        
        try:
            # PASO 1: AGREGACIÓN POR CLIENTE
            # ===============================
            # Consolidamos todas las citas de cada cliente en una fila
            # De: 2000 citas → A: 150 clientes con sus estadísticas
            clientes_stats = df.groupby('client_id').agg({
                'appointment_id': 'count',  # Frecuencia: cuántas veces vino
                'precio_servicio': 'sum',    # Gasto total: $$ que ha gastado
                'asistio': 'mean',           # Lealtad: % de citas a las que asistió
                'edad_mascota': 'mean'       # Edad promedio de sus mascotas
            }).reset_index()
            
            # Renombrar columnas para claridad
            clientes_stats.columns = ['client_id', 'total_citas', 'gasto_total', 
                                     'tasa_asistencia', 'edad_promedio_mascotas']
            
            # Limpiar datos: eliminar clientes con datos faltantes
            clientes_stats = clientes_stats.dropna()
            
            # Validar datos suficientes
            if len(clientes_stats) < n_clusters:
                return {"error": "Clientes insuficientes para clustering"}
            
            # PASO 2: SELECCIÓN DE FEATURES
            # ==============================
            # Elegimos las características que definen el comportamiento del cliente
            # - total_citas: Frecuencia de visitas
            # - gasto_total: Valor económico del cliente
            # - tasa_asistencia: Confiabilidad del cliente
            X = clientes_stats[['total_citas', 'gasto_total', 'tasa_asistencia']].values
            
            # PASO 3: NORMALIZACIÓN (StandardScaler)
            # =======================================
            # Problema: Features en diferentes escalas
            #   total_citas: 1-20 (rango pequeño)
            #   gasto_total: 50-5000 (rango grande)
            # 
            # Solución: Estandarizar todo a media=0, std=1
            # Fórmula: z = (valor - media) / desviación_estándar
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # PASO 4: CLUSTERING JERÁRQUICO
            # ==============================
            # Algoritmo: Agglomerative (bottom-up)
            # Proceso:
            #   1. Inicio: Cada cliente = 1 cluster (150 clusters)
            #   2. Iteración: Une los 2 clusters más cercanos
            #   3. Repite hasta tener n_clusters grupos (4 en este caso)
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,    # Número final de segmentos (4)
                linkage='average',        # Método: promedio de distancias
                metric='euclidean'        # Distancia: euclidiana (d = √(Δx² + Δy² + Δz²))
            )
            
            # Ejecutar clustering y asignar etiquetas
            # labels = [0, 0, 1, 2, 0, 1, 3, 2, ...] (un número por cliente)
            labels = clustering.fit_predict(X_scaled)
            clientes_stats['segmento'] = labels
            
            # PASO 5: EVALUAR CALIDAD
            # ========================
            # Silhouette Score: Métrica de validación interna
            # Pregunta: ¿Qué tan bien separados están los clusters?
            # Fórmula: s = (b - a) / max(a, b)
            #   a = distancia promedio dentro del cluster
            #   b = distancia al cluster más cercano
            # Interpretación:
            #   0.7-1.0 = Excelente separación
            #   0.5-0.7 = Buena separación
            #   0.3-0.5 = Moderada
            #   < 0.3   = Mala (clusters solapados)
            silhouette_avg = silhouette_score(X_scaled, labels)
            
            # Caracterizar cada segmento
            segmentos_info = []
            nombres_segmentos = {
                0: "VIP - Alta frecuencia",
                1: "Regular - Moderado",
                2: "Ocasional - Bajo",
                3: "Nuevo - Exploratorio"
            }
            
            for i in range(n_clusters):
                segmento_data = clientes_stats[clientes_stats['segmento'] == i]
                
                # Determinar perfil del segmento
                citas_promedio = segmento_data['total_citas'].mean()
                gasto_promedio = segmento_data['gasto_total'].mean()
                
                segmentos_info.append({
                    "segmento_id": int(i),
                    "nombre": nombres_segmentos.get(i, f"Segmento {i}"),
                    "total_clientes": len(segmento_data),
                    "citas_promedio": float(citas_promedio),
                    "gasto_promedio": float(gasto_promedio),
                    "tasa_asistencia_promedio": float(segmento_data['tasa_asistencia'].mean()),
                    "valor_total_segmento": float(segmento_data['gasto_total'].sum())
                })
            
            # Ordenar por valor
            segmentos_info = sorted(segmentos_info, key=lambda x: x['gasto_promedio'], reverse=True)
            
            logger.info(f"✓ Segmentación completada. Silhouette Score: {silhouette_avg:.3f}")
            
            return {
                "n_segmentos": n_clusters,
                "total_clientes_analizados": len(clientes_stats),
                "silhouette_score": float(silhouette_avg),
                "segmentos": segmentos_info,
                "metodo": "Agglomerative (Average)",
                "calidad_clustering": "Buena" if silhouette_avg > 0.5 else "Moderada" if silhouette_avg > 0.3 else "Baja"
            }
            
        except Exception as e:
            logger.error(f"❌ Error en clustering de clientes: {e}")
            return {"error": str(e)}
    
    def clustering_servicios(self, df: pd.DataFrame, n_clusters: int = 3) -> Dict:
        """
        Clustering de servicios por patrones de uso
        Agrupa servicios según horarios, frecuencia y tipo de mascota
        
        Args:
            df: DataFrame con datos de citas
            n_clusters: Número de grupos de servicios
            
        Returns:
            Dict con análisis de grupos de servicios
        """
        logger.info(f"🔬 Agrupando servicios con Hierarchical Clustering ({n_clusters} grupos)...")
        
        try:
            # Agrupar por servicio
            servicios_stats = df.groupby('service_id').agg({
                'appointment_id': 'count',  # Frecuencia
                'hora': 'mean',              # Hora promedio
                'dia_semana': 'mean',        # Día promedio
                'asistio': 'mean',           # Tasa de asistencia
                'edad_mascota': 'mean'       # Edad promedio
            }).reset_index()
            
            servicios_stats.columns = ['service_id', 'total_uso', 'hora_promedio', 
                                      'dia_promedio', 'tasa_asistencia', 'edad_promedio']
            
            # Agregar nombre del servicio
            servicios_nombre = df.groupby('service_id')['servicio'].first()
            servicios_stats = servicios_stats.merge(
                servicios_nombre, 
                left_on='service_id', 
                right_index=True, 
                how='left'
            )
            
            if len(servicios_stats) < n_clusters:
                n_clusters = len(servicios_stats)
            
            # Features para clustering
            X = servicios_stats[['total_uso', 'hora_promedio', 'tasa_asistencia']].values
            
            # Estandarizar
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Clustering
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage='complete',
                metric='euclidean'
            )
            
            labels = clustering.fit_predict(X_scaled)
            servicios_stats['grupo'] = labels
            
            # Métricas
            silhouette_avg = silhouette_score(X_scaled, labels) if len(set(labels)) > 1 else 0
            
            # Analizar grupos
            grupos_info = []
            for i in range(n_clusters):
                grupo_data = servicios_stats[servicios_stats['grupo'] == i]
                
                grupos_info.append({
                    "grupo_id": int(i),
                    "total_servicios": len(grupo_data),
                    "servicios": grupo_data['servicio'].tolist(),
                    "uso_promedio": float(grupo_data['total_uso'].mean()),
                    "hora_promedio": float(grupo_data['hora_promedio'].mean()),
                    "tasa_asistencia_promedio": float(grupo_data['tasa_asistencia'].mean())
                })
            
            logger.info(f"✓ Agrupación de servicios completada. Silhouette: {silhouette_avg:.3f}")
            
            return {
                "n_grupos": n_clusters,
                "total_servicios": len(servicios_stats),
                "silhouette_score": float(silhouette_avg),
                "grupos": grupos_info,
                "metodo": "Agglomerative (Complete)"
            }
            
        except Exception as e:
            logger.error(f"❌ Error en clustering de servicios: {e}")
            return {"error": str(e)}
    
    def analisis_clustering_completo(self, df: pd.DataFrame) -> Dict:
        """
        Realiza análisis de clustering jerárquico completo
        Incluye clustering de mascotas, clientes y servicios
        
        Returns:
            Dict con todos los análisis de clustering
        """
        logger.info("\n" + "=" * 80)
        logger.info("🔬 ANÁLISIS DE HIERARCHICAL CLUSTERING COMPLETO")
        logger.info("=" * 80)
        
        resultados = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "total_registros": len(df),
            "clustering_mascotas": self.clustering_mascotas(df, n_clusters=3),
            "clustering_clientes": self.clustering_clientes(df, n_clusters=4),
            "clustering_servicios": self.clustering_servicios(df, n_clusters=3)
        }
        
        logger.info("\n✅ Análisis de clustering completado")
        
        return resultados
    
    # =========================================================================
    # GUARDAR Y CARGAR MODELOS
    # =========================================================================
    
    def guardar_modelos(self):
        """Guarda los modelos entrenados"""
        logger.info("\n💾 Guardando modelos...")
        
        if self.model_tipo_mascota:
            self.model_tipo_mascota.save(PATHS['predictor_model'])
            logger.info("✓ Modelo tipo mascota guardado")
        
        # Guardar encoders y scaler
        with open(PATHS['scaler'], 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'label_encoder_tipo': self.label_encoder_tipo
            }, f)
        
        logger.info("✓ Encoders y scaler guardados")
        self.trained = True
    
    def cargar_modelos(self):
        """Carga modelos previamente entrenados"""
        try:
            logger.info("📂 Cargando modelos...")
            
            self.model_tipo_mascota = load_model(PATHS['predictor_model'])
            
            with open(PATHS['scaler'], 'rb') as f:
                data = pickle.load(f)
                self.scaler = data['scaler']
                self.label_encoder_tipo = data['label_encoder_tipo']
            
            self.trained = True
            logger.info("✓ Modelos cargados exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error cargando modelos: {e}")
            self.trained = False


# =============================================================================
# FUNCIÓN DE PRUEBA
# =============================================================================
if __name__ == "__main__":
    from database import PetStoreDatabase
    
    print("=" * 80)
    print("🧠 ENTRENANDO MODELOS DE PREDICCIÓN")
    print("=" * 80)
    
    # Conectar a BD y obtener datos
    db = PetStoreDatabase()
    df = db.obtener_dataset_completo()
    
    print(f"\n📊 Dataset cargado: {len(df)} registros")
    
    if len(df) > 0:
        # Crear predictor
        predictor = PetStorePredictor()
        
        # Análisis básicos
        print("\n" + "=" * 80)
        print("📊 ANÁLISIS ESTADÍSTICO")
        print("=" * 80)
        
        print("\n🐾 Tipo de mascota más común:")
        analisis_tipo = predictor.analizar_tipo_mascota_mas_comun(df)
        for stat in analisis_tipo['estadisticas'][:5]:
            print(f"   {stat['tipo']}: {stat['cantidad']} ({stat['porcentaje']}%)")
        
        print("\n📅 Día con más atención:")
        analisis_dia = predictor.analizar_dia_mas_atencion(df)
        print(f"   {analisis_dia['dia_con_mas_atencion']}")
        
        print("\n⏰ Hora pico:")
        analisis_hora = predictor.analizar_hora_pico(df)
        print(f"   {analisis_hora['hora_pico']}:00 horas")
        
        # Entrenar modelos
        print("\n" + "=" * 80)
        print("🚀 ENTRENANDO MODELOS")
        print("=" * 80)
        
        # Modelo 1: Tipo de mascota
        resultado1 = predictor.entrenar_modelo_tipo_mascota(df)
        
        # Modelo 2: Asistencia
        resultado2 = predictor.entrenar_modelo_asistencia(df)
        
        # Guardar modelos
        predictor.guardar_modelos()
        
        print("\n" + "=" * 80)
        print("✅ ENTRENAMIENTO COMPLETADO")
        print("=" * 80)
    else:
        print("\n❌ No hay datos suficientes para entrenar")

