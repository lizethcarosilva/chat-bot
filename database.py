"""
MÓDULO DE BASE DE DATOS
Conexión y consultas a PostgreSQL del Pet Store
"""

import psycopg2
import pandas as pd
from typing import Optional, Dict, List
import logging
from config import DB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PetStoreDatabase:
    """Gestiona la conexión y consultas a la base de datos PostgreSQL"""
    
    def __init__(self):
        self.conn = None
        self.conectar()
    
    def conectar(self):
        """Establece conexión con PostgreSQL"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            logger.info(" Conexión exitosa a PostgreSQL")
        except Exception as e:
            logger.error(f" Error de conexión: {e}")
            raise
    
    def ejecutar_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Ejecuta una consulta y retorna un DataFrame"""
        try:
            # Verificar si la conexión está cerrada y reconectar
            if self.conn is None or self.conn.closed:
                logger.warning("  Conexión cerrada, reconectando...")
                self.conectar()
            
            if params:
                df = pd.read_sql(query, self.conn, params=params)
            else:
                df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            logger.error(f" Error ejecutando query: {e}")
            # Intentar reconectar una vez más
            try:
                logger.info(" Intentando reconectar...")
                self.conectar()
                if params:
                    df = pd.read_sql(query, self.conn, params=params)
                else:
                    df = pd.read_sql(query, self.conn)
                return df
            except Exception as e2:
                logger.error(f" Error en segundo intento: {e2}")
                return pd.DataFrame()
    
    # =========================================================================
    # CONSULTAS PARA ANÁLISIS PREDICTIVO
    # =========================================================================
    
    def obtener_dataset_completo(self) -> pd.DataFrame:
        """
        Obtiene dataset completo para Machine Learning
        Incluye: citas, mascotas, servicios, clientes
        """
        # Construyo una consulta SQL compleja que obtiene todos los datos necesarios para machine learning
        query = """
        SELECT 
            -- Selecciono los identificadores únicos de cada entidad
            a.appointment_id,  -- ID único de la cita para rastrear cada registro
            a.pet_id,  -- ID de la mascota para relacionar con su información
            a.client_id,  -- ID del cliente dueño de la mascota
            a.service_id,  -- ID del servicio contratado
            
            -- Extraigo características temporales que son importantes para predecir patrones
            a.fecha_hora AS fecha_cita,  -- Fecha y hora completa de la cita
            EXTRACT(YEAR FROM a.fecha_hora) AS año,  -- Año de la cita para análisis de tendencias anuales
            EXTRACT(MONTH FROM a.fecha_hora) AS mes,  -- Mes (1-12) para identificar estacionalidad
            EXTRACT(DAY FROM a.fecha_hora) AS dia,  -- Día del mes (1-31)
            EXTRACT(DOW FROM a.fecha_hora) AS dia_semana,  -- Día de la semana (0-6) para patrones semanales
            EXTRACT(HOUR FROM a.fecha_hora) AS hora,  -- Hora del día (0-23) para identificar horas pico
            EXTRACT(WEEK FROM a.fecha_hora) AS semana_del_año,  -- Número de semana del año (1-52)
            
            -- Obtengo información del servicio que impacta en el análisis
            s.nombre AS servicio,  -- Nombre descriptivo del servicio (baño, vacuna, consulta, etc.)
            s.precio AS precio_servicio,  -- Precio del servicio como feature económico
            s.duracion_minutos,  -- Duración estimada para planificación de recursos
            
            -- Extraigo características de la mascota que son relevantes para predicciones
            p.tipo AS tipo_mascota,  -- Tipo de mascota (perro, gato, conejo, etc.)
            p.raza,  -- Raza específica de la mascota
            p.edad AS edad_mascota,  -- Edad en años, importante para tipos de servicios
            p.sexo AS sexo_mascota,  -- Sexo de la mascota
            
            -- Obtengo el estado de la cita que usaremos como variable objetivo en ML
            a.estado,  -- Estado actual de la cita (COMPLETADA, CANCELADA, PROGRAMADA, etc.)
            CASE WHEN a.estado = 'COMPLETADA' THEN 1 ELSE 0 END AS asistio,  -- Variable binaria: 1 si asistió, 0 si no
            CASE WHEN a.estado = 'CANCELADA' THEN 1 ELSE 0 END AS cancelo  -- Variable binaria: 1 si canceló, 0 si no
            
        FROM appointment a  -- Tabla principal de citas
        JOIN service s ON a.service_id = s.service_id  -- Uno con servicios para obtener detalles del servicio
        JOIN pet p ON a.pet_id = p.pet_id  -- Uno con mascotas para obtener características de la mascota
        JOIN client c ON a.client_id = c.client_id  -- Uno con clientes para validar que el cliente existe
        WHERE a.activo = true  -- Solo incluyo citas activas, excluyendo registros eliminados
        ORDER BY a.fecha_hora DESC;  -- Ordeno por fecha descendente para tener las más recientes primero
        """
        
        # Registro en el log que estoy obteniendo el dataset para machine learning
        logger.info(" Obteniendo dataset completo para ML...")
        # Ejecuto la consulta SQL y obtengo los resultados en un DataFrame de pandas
        df = self.ejecutar_query(query)
        # Registro cuántos registros obtuve para validar la cantidad de datos disponibles
        logger.info(f" Dataset obtenido: {len(df)} registros")
        # Retorno el DataFrame completo listo para ser usado en modelos de machine learning
        return df
    
    def obtener_tipos_mascota_mas_comunes(self) -> pd.DataFrame:
        """Obtiene estadísticas de tipos de mascotas"""
        # Creo una consulta SQL compleja que analiza los diferentes tipos de mascotas
        query = """
        SELECT 
            p.tipo AS tipo_mascota,  -- Extraigo el tipo de mascota (perro, gato, conejo, etc.)
            COUNT(DISTINCT p.pet_id) AS total_mascotas,  -- Cuento cuántas mascotas únicas hay de cada tipo
            COUNT(a.appointment_id) AS total_citas,  -- Cuento el total de citas que ha tenido este tipo de mascota
            ROUND(COUNT(a.appointment_id)::numeric / 
                  NULLIF(COUNT(DISTINCT p.pet_id), 0), 2) AS promedio_citas_por_mascota,  -- Calculo el promedio de citas por mascota de este tipo
            ROUND(COUNT(DISTINCT p.pet_id)::numeric * 100.0 / 
                  (SELECT COUNT(*) FROM pet WHERE activo = true), 2) AS porcentaje  -- Calculo qué porcentaje representa este tipo del total de mascotas
        FROM pet p  -- Tabla principal de mascotas
        LEFT JOIN appointment a ON p.pet_id = a.pet_id AND a.activo = true  -- Uno con las citas para obtener estadísticas de uso
        WHERE p.activo = true  -- Solo considero mascotas activas en el sistema
        GROUP BY p.tipo  -- Agrupo los resultados por tipo de mascota para obtener totales
        ORDER BY total_mascotas DESC;  -- Ordeno de mayor a menor para ver los tipos más comunes primero
        """
        
        # Registro en el log que estoy consultando los tipos de mascotas
        logger.info(" Obteniendo tipos de mascotas...")
        # Ejecuto la consulta y retorno el DataFrame con los resultados
        return self.ejecutar_query(query)
    
    def obtener_dias_con_mas_atencion(self) -> pd.DataFrame:
        """Obtiene estadísticas por día de la semana"""
        # Construyo una consulta SQL que analiza el comportamiento por día de la semana
        query = """
        SELECT 
            CASE EXTRACT(DOW FROM a.fecha_hora)  -- Extraigo el día de la semana de la fecha (0-6)
                WHEN 0 THEN 'Domingo'  -- Convierto el número 0 en el nombre del día
                WHEN 1 THEN 'Lunes'    -- Transformo cada número en su correspondiente nombre
                WHEN 2 THEN 'Martes'
                WHEN 3 THEN 'Miércoles'
                WHEN 4 THEN 'Jueves'
                WHEN 5 THEN 'Viernes'
                WHEN 6 THEN 'Sábado'
            END AS dia_semana,  -- Guardo el nombre del día en formato legible
            EXTRACT(DOW FROM a.fecha_hora) AS numero_dia,  -- Mantengo también el número del día (0-6) para ordenamiento
            COUNT(a.appointment_id) AS total_citas,  -- Cuento cuántas citas hay en total ese día
            COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END) AS completadas,  -- Cuento solo las citas que se realizaron exitosamente
            COUNT(CASE WHEN a.estado = 'CANCELADA' THEN 1 END) AS canceladas,  -- Cuento cuántas citas fueron canceladas ese día
            ROUND(AVG(EXTRACT(HOUR FROM a.fecha_hora)), 2) AS hora_promedio,  -- Calculo a qué hora promedio se dan las citas ese día
            ROUND(COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END)::numeric * 100.0 / 
                  NULLIF(COUNT(a.appointment_id), 0), 2) AS tasa_asistencia  -- Calculo el porcentaje de citas completadas vs totales
        FROM appointment a  -- Consulto la tabla de citas
        WHERE a.activo = true  -- Solo considero citas activas en el sistema
        GROUP BY EXTRACT(DOW FROM a.fecha_hora)  -- Agrupo todos los resultados por día de la semana
        ORDER BY numero_dia;  -- Ordeno de domingo a sábado para visualización cronológica
        """
        
        # Registro en el log que estoy obteniendo estadísticas de días
        logger.info(" Obteniendo días con más atención...")
        # Ejecuto la consulta SQL y retorno los resultados en un DataFrame
        return self.ejecutar_query(query)
    
    def obtener_horas_pico(self) -> pd.DataFrame:
        """Obtiene estadísticas por hora del día"""
        # Creo una consulta SQL para analizar la distribución de citas por hora del día
        query = """
        SELECT 
            EXTRACT(HOUR FROM a.fecha_hora) AS hora,  -- Extraigo solo la hora (0-23) de la fecha y hora de la cita
            COUNT(a.appointment_id) AS total_citas,  -- Cuento cuántas citas hay programadas en esa hora
            COUNT(DISTINCT a.pet_id) AS mascotas_unicas,  -- Cuento cuántas mascotas diferentes han tenido citas en esa hora
            COUNT(DISTINCT a.client_id) AS clientes_unicos,  -- Cuento cuántos clientes distintos visitaron en esa hora
            ROUND(AVG(s.duracion_minutos), 2) AS duracion_promedio  -- Calculo la duración promedio de los servicios en esa hora
        FROM appointment a  -- Consulto la tabla principal de citas
        JOIN service s ON a.service_id = s.service_id  -- Uno con servicios para obtener información de duración
        WHERE a.activo = true  -- Solo considero citas activas en el sistema
        GROUP BY hora  -- Agrupo todos los resultados por hora del día
        ORDER BY hora;  -- Ordeno cronológicamente de 0 (medianoche) a 23 (11pm)
        """
        
        # Registro en el log que estoy consultando las horas pico
        logger.info("⏰ Obteniendo horas pico...")
        # Ejecuto la consulta y retorno el DataFrame con las estadísticas horarias
        return self.ejecutar_query(query)
    
    def obtener_servicios_mas_utilizados(self) -> pd.DataFrame:
        """Obtiene ranking de servicios más solicitados"""
        query = """
        SELECT 
            s.service_id,
            s.nombre AS servicio,
            s.precio,
            COUNT(a.appointment_id) AS total_citas,
            COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END) AS completadas,
            COUNT(CASE WHEN a.estado = 'CANCELADA' THEN 1 END) AS canceladas,
            ROUND(COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END)::numeric * 100.0 / 
                  NULLIF(COUNT(a.appointment_id), 0), 2) AS tasa_asistencia,
            ROUND(AVG(s.precio), 2) AS precio_promedio
        FROM appointment a
        JOIN service s ON a.service_id = s.service_id
        WHERE a.activo = true
        GROUP BY s.service_id, s.nombre, s.precio
        ORDER BY total_citas DESC;
        """
        
        logger.info(" Obteniendo servicios más utilizados...")
        return self.ejecutar_query(query)
    
    def obtener_razas_por_tipo(self, tipo_mascota: str) -> pd.DataFrame:
        """Obtiene las razas más comunes de un tipo de mascota"""
        query = """
        SELECT 
            p.raza,
            COUNT(*) AS cantidad,
            ROUND(AVG(p.edad), 1) AS edad_promedio,
            COUNT(a.appointment_id) AS total_servicios
        FROM pet p
        LEFT JOIN appointment a ON p.pet_id = a.pet_id AND a.activo = true
        WHERE p.activo = true AND LOWER(p.tipo) = LOWER(%s)
        GROUP BY p.raza
        ORDER BY cantidad DESC
        LIMIT 10;
        """
        
        logger.info(f" Obteniendo razas de {tipo_mascota}...")
        return self.ejecutar_query(query, (tipo_mascota,))
    
    # =========================================================================
    # CONSULTAS PARA CHATBOT
    # =========================================================================
    
    def buscar_mascota_por_nombre(self, nombre: str) -> pd.DataFrame:
        """Busca mascotas por nombre"""
        query = """
        SELECT 
            p.pet_id,
            p.nombre,
            p.tipo,
            p.raza,
            p.edad,
            p.sexo,
            c.name as propietario,
            c.telefono,
            c.correo
        FROM pet p
        JOIN pet_owner po ON p.pet_id = po.pet_id
        JOIN client c ON po.client_id = c.client_id
        WHERE LOWER(p.nombre) LIKE LOWER(%s) AND p.activo = true
        LIMIT 10;
        """
        
        return self.ejecutar_query(query, (f'%{nombre}%',))
    
    def obtener_historial_mascota(self, pet_id: int) -> pd.DataFrame:
        """Obtiene historial médico de una mascota"""
        query = """
        SELECT 
            pmh.fecha_atencion,
            s.nombre as servicio,
            pmh.tipo_procedimiento,
            pmh.diagnostico,
            pmh.tratamiento,
            u.name as veterinario
        FROM pet_medical_history pmh
        JOIN service s ON pmh.service_id = s.service_id
        JOIN "user" u ON pmh.veterinarian_id = u.user_id
        WHERE pmh.pet_id = %s AND pmh.activo = true
        ORDER BY pmh.fecha_atencion DESC
        LIMIT 20;
        """
        
        return self.ejecutar_query(query, (pet_id,))
    
    def obtener_proximas_citas_mascota(self, pet_id: int) -> pd.DataFrame:
        """Obtiene próximas citas de una mascota"""
        query = """
        SELECT 
            a.fecha_hora,
            s.nombre as servicio,
            a.estado,
            u.name as veterinario,
            a.observaciones
        FROM appointment a
        JOIN service s ON a.service_id = s.service_id
        LEFT JOIN "user" u ON a.veterinarian_id = u.user_id
        WHERE a.pet_id = %s
          AND a.fecha_hora >= CURRENT_DATE
          AND a.estado IN ('PROGRAMADA', 'EN_PROCESO')
          AND a.activo = true
        ORDER BY a.fecha_hora
        LIMIT 10;
        """
        
        return self.ejecutar_query(query, (pet_id,))
    
    def obtener_vacunas_mascota(self, pet_id: int) -> pd.DataFrame:
        """Obtiene historial de vacunación"""
        query = """
        SELECT 
            v.vaccine_name as vacuna,
            v.application_date as fecha_aplicacion,
            v.next_dose_date as proxima_dosis,
            v.dose_number as dosis_numero,
            v.estado,
            u.name as veterinario
        FROM vaccination v
        JOIN "user" u ON v.veterinarian_id = u.user_id
        WHERE v.pet_id = %s AND v.activo = true
        ORDER BY v.application_date DESC
        LIMIT 20;
        """
        
        return self.ejecutar_query(query, (pet_id,))
    
    def buscar_cliente_por_correo(self, correo: str) -> pd.DataFrame:
        """Busca cliente por correo electrónico"""
        query = """
        SELECT 
            client_id,
            name,
            correo,
            telefono,
            direccion
        FROM client
        WHERE LOWER(correo) = LOWER(%s) AND activo = true;
        """
        
        return self.ejecutar_query(query, (correo,))
    
    def obtener_mascotas_cliente(self, client_id: int) -> pd.DataFrame:
        """Obtiene todas las mascotas de un cliente"""
        query = """
        SELECT 
            p.pet_id,
            p.nombre,
            p.tipo,
            p.raza,
            p.edad,
            p.sexo,
            p.color
        FROM pet p
        JOIN pet_owner po ON p.pet_id = po.pet_id
        WHERE po.client_id = %s AND p.activo = true
        ORDER BY p.nombre;
        """
        
        return self.ejecutar_query(query, (client_id,))
    
    def obtener_servicios_disponibles(self) -> pd.DataFrame:
        """Lista todos los servicios disponibles"""
        query = """
        SELECT 
            service_id,
            nombre,
            descripcion,
            precio,
            duracion_minutos
        FROM service
        WHERE activo = true
        ORDER BY nombre;
        """
        
        return self.ejecutar_query(query)
    
    # =========================================================================
    # ESTADÍSTICAS GENERALES
    # =========================================================================
    
    def obtener_estadisticas_generales(self) -> Dict:
        """Obtiene estadísticas generales del sistema"""
        # Creo un diccionario vacío donde almacenaré todas las métricas del sistema
        stats = {}
        
        # Consulto cuántas mascotas activas hay registradas en la base de datos
        query_mascotas = "SELECT COUNT(*) as total FROM pet WHERE activo = true"
        # Ejecuto la consulta y obtengo el resultado en un DataFrame de pandas
        df_mascotas = self.ejecutar_query(query_mascotas)
        # Extraigo el número total de mascotas, usando 0 si no hay resultados
        stats['total_mascotas'] = int(df_mascotas.iloc[0]['total']) if not df_mascotas.empty else 0
        
        # Consulto la cantidad de clientes activos registrados en el sistema
        query_clientes = "SELECT COUNT(*) as total FROM client WHERE activo = true"
        # Ejecuto la consulta SQL para contar clientes
        df_clientes = self.ejecutar_query(query_clientes)
        # Guardo el total de clientes en el diccionario de estadísticas
        stats['total_clientes'] = int(df_clientes.iloc[0]['total']) if not df_clientes.empty else 0
        
        # Consulto el número total de citas programadas que están activas
        query_citas = "SELECT COUNT(*) as total FROM appointment WHERE activo = true"
        # Ejecuto la query para obtener el conteo de citas
        df_citas = self.ejecutar_query(query_citas)
        # Almaceno el total de citas en las estadísticas generales
        stats['total_citas'] = int(df_citas.iloc[0]['total']) if not df_citas.empty else 0
        
        # Consulto cuántos servicios diferentes ofrece la veterinaria
        query_servicios = "SELECT COUNT(*) as total FROM service WHERE activo = true"
        # Ejecuto la consulta para contar los servicios disponibles
        df_servicios = self.ejecutar_query(query_servicios)
        # Guardo la cantidad de servicios disponibles en el diccionario
        stats['total_servicios'] = int(df_servicios.iloc[0]['total']) if not df_servicios.empty else 0
        
        # Retorno el diccionario completo con todas las estadísticas del sistema
        return stats
    
    # =========================================================================
    # MÉTRICAS DE NEGOCIO Y VENTAS
    # =========================================================================
    
    def obtener_citas_hoy(self) -> pd.DataFrame:
        """
        Obtiene las citas programadas para hoy
        
        Returns:
            DataFrame con citas del día actual
        """
        query = """
        SELECT 
            a.appointment_id,
            a.fecha_hora,
            EXTRACT(HOUR FROM a.fecha_hora) AS hora,
            p.nombre AS mascota,
            p.tipo AS tipo_mascota,
            c.name AS cliente,
            c.telefono,
            s.nombre AS servicio,
            s.precio,
            a.estado,
            u.name AS veterinario
        FROM appointment a
        JOIN pet p ON a.pet_id = p.pet_id
        JOIN client c ON a.client_id = c.client_id
        JOIN service s ON a.service_id = s.service_id
        LEFT JOIN "user" u ON a.veterinarian_id = u.user_id
        WHERE DATE(a.fecha_hora) = CURRENT_DATE
          AND a.activo = true
        ORDER BY a.fecha_hora;
        """
        
        logger.info(" Obteniendo citas de hoy...")
        return self.ejecutar_query(query)
    
    def obtener_cantidad_productos(self) -> int:
        """
        Obtiene la cantidad total de productos en inventario
        
        Returns:
            Total de productos únicos
        """
        query = """
        SELECT COUNT(*) as total
        FROM producto
        WHERE activo = true;
        """
        
        try:
            df = self.ejecutar_query(query)
            total = int(df.iloc[0]['total']) if not df.empty else 0
            logger.info(f" Total de productos: {total}")
            return total
        except Exception as e:
            logger.warning(f"  Tabla 'producto' no existe: {e}")
            return 0
    
    def obtener_ventas_dia(self) -> Dict:
        """
        Obtiene las ventas del día actual
        
        Returns:
            Dict con total de ventas, cantidad de transacciones y productos vendidos
        """
        query = """
        SELECT 
            COUNT(DISTINCT v.venta_id) AS total_transacciones,
            COUNT(dv.detalle_id) AS total_items_vendidos,
            COALESCE(SUM(dv.cantidad), 0) AS cantidad_productos,
            COALESCE(SUM(dv.subtotal), 0) AS total_ventas,
            COALESCE(AVG(dv.precio_unitario), 0) AS ticket_promedio
        FROM venta v
        JOIN detalle_venta dv ON v.venta_id = dv.venta_id
        WHERE DATE(v.fecha_venta) = CURRENT_DATE
          AND v.activo = true;
        """
        
        try:
            df = self.ejecutar_query(query)
            
            if df.empty:
                return {
                    'total_ventas': 0,
                    'total_transacciones': 0,
                    'total_items_vendidos': 0,
                    'cantidad_productos': 0,
                    'ticket_promedio': 0
                }
            
            row = df.iloc[0]
            resultado = {
                'total_ventas': float(row['total_ventas']),
                'total_transacciones': int(row['total_transacciones']),
                'total_items_vendidos': int(row['total_items_vendidos']),
                'cantidad_productos': int(row['cantidad_productos']),
                'ticket_promedio': float(row['ticket_promedio'])
            }
            
            logger.info(f" Ventas del día: ${resultado['total_ventas']:,.2f}")
            return resultado
            
        except Exception as e:
            logger.warning(f"  Error obteniendo ventas del día: {e}")
            return {
                'total_ventas': 0,
                'total_transacciones': 0,
                'total_items_vendidos': 0,
                'cantidad_productos': 0,
                'ticket_promedio': 0
            }
    
    def obtener_ventas_mes(self) -> Dict:
        """
        Obtiene las ventas del mes actual
        
        Returns:
            Dict con estadísticas de ventas del mes
        """
        query = """
        SELECT 
            COUNT(DISTINCT v.venta_id) AS total_transacciones,
            COUNT(dv.detalle_id) AS total_items_vendidos,
            COALESCE(SUM(dv.cantidad), 0) AS cantidad_productos,
            COALESCE(SUM(dv.subtotal), 0) AS total_ventas,
            COALESCE(AVG(dv.precio_unitario), 0) AS ticket_promedio,
            COUNT(DISTINCT v.client_id) AS clientes_unicos
        FROM venta v
        JOIN detalle_venta dv ON v.venta_id = dv.venta_id
        WHERE EXTRACT(YEAR FROM v.fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
          AND EXTRACT(MONTH FROM v.fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
          AND v.activo = true;
        """
        
        try:
            df = self.ejecutar_query(query)
            
            if df.empty:
                return {
                    'total_ventas': 0,
                    'total_transacciones': 0,
                    'total_items_vendidos': 0,
                    'cantidad_productos': 0,
                    'ticket_promedio': 0,
                    'clientes_unicos': 0
                }
            
            row = df.iloc[0]
            resultado = {
                'total_ventas': float(row['total_ventas']),
                'total_transacciones': int(row['total_transacciones']),
                'total_items_vendidos': int(row['total_items_vendidos']),
                'cantidad_productos': int(row['cantidad_productos']),
                'ticket_promedio': float(row['ticket_promedio']),
                'clientes_unicos': int(row['clientes_unicos'])
            }
            
            logger.info(f" Ventas del mes: ${resultado['total_ventas']:,.2f}")
            return resultado
            
        except Exception as e:
            logger.warning(f"  Error obteniendo ventas del mes: {e}")
            return {
                'total_ventas': 0,
                'total_transacciones': 0,
                'total_items_vendidos': 0,
                'cantidad_productos': 0,
                'ticket_promedio': 0,
                'clientes_unicos': 0
            }
    
    def obtener_productos_proximos_vencer(self, dias: int = 30) -> pd.DataFrame:
        """
        Obtiene productos próximos a vencer
        
        Args:
            dias: Días de anticipación para alertar (default: 30)
            
        Returns:
            DataFrame con productos próximos a vencer
        """
        query = """
        SELECT 
            p.producto_id,
            p.nombre AS producto,
            p.categoria,
            p.fecha_vencimiento,
            p.stock_actual,
            p.precio_venta,
            (DATE(p.fecha_vencimiento) - CURRENT_DATE) AS dias_hasta_vencer,
            (p.stock_actual * p.precio_venta) AS valor_inventario
        FROM producto p
        WHERE p.fecha_vencimiento IS NOT NULL
          AND DATE(p.fecha_vencimiento) BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '%s days'
          AND p.activo = true
          AND p.stock_actual > 0
        ORDER BY p.fecha_vencimiento ASC;
        """
        
        try:
            logger.info(f"  Buscando productos próximos a vencer (en {dias} días)...")
            df = self.ejecutar_query(query % dias)
            logger.info(f"   Encontrados: {len(df)} productos")
            return df
        except Exception as e:
            logger.warning(f"  Error obteniendo productos próximos a vencer: {e}")
            return pd.DataFrame()
    
    def obtener_alerta_bajo_inventario(self) -> pd.DataFrame:
        """
        Obtiene productos con bajo inventario (stock actual < stock mínimo)
        
        Returns:
            DataFrame con productos en alerta de bajo inventario
        """
        query = """
        SELECT 
            p.producto_id,
            p.nombre AS producto,
            p.categoria,
            p.stock_actual,
            p.stock_minimo,
            p.stock_maximo,
            (p.stock_minimo - p.stock_actual) AS unidades_faltantes,
            ROUND((p.stock_actual::numeric / NULLIF(p.stock_minimo, 0)) * 100, 2) AS porcentaje_stock,
            p.precio_compra,
            ((p.stock_minimo - p.stock_actual) * p.precio_compra) AS costo_reposicion,
            p.proveedor
        FROM producto p
        WHERE p.stock_actual < p.stock_minimo
          AND p.activo = true
        ORDER BY porcentaje_stock ASC, p.stock_actual ASC;
        """
        
        try:
            logger.info(" Verificando alertas de bajo inventario...")
            df = self.ejecutar_query(query)
            logger.info(f"   Alertas: {len(df)} productos con bajo inventario")
            return df
        except Exception as e:
            logger.warning(f"  Error obteniendo alertas de inventario: {e}")
            return pd.DataFrame()
    
    def obtener_comparativa_ventas_mensual(self) -> Dict:
        """
        Obtiene comparativa de ventas: Mes actual vs mes anterior
        
        Returns:
            Dict con comparativa de ventas mensuales
        """
        query = """
        WITH ventas_mes_actual AS (
            SELECT 
                COUNT(DISTINCT v.venta_id) AS transacciones,
                COALESCE(SUM(dv.subtotal), 0) AS total_ventas
            FROM venta v
            JOIN detalle_venta dv ON v.venta_id = dv.venta_id
            WHERE EXTRACT(YEAR FROM v.fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
              AND EXTRACT(MONTH FROM v.fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
              AND v.activo = true
        ),
        ventas_mes_anterior AS (
            SELECT 
                COUNT(DISTINCT v.venta_id) AS transacciones,
                COALESCE(SUM(dv.subtotal), 0) AS total_ventas
            FROM venta v
            JOIN detalle_venta dv ON v.venta_id = dv.venta_id
            WHERE EXTRACT(YEAR FROM v.fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month')
              AND EXTRACT(MONTH FROM v.fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month')
              AND v.activo = true
        )
        SELECT 
            ma.total_ventas AS ventas_mes_actual,
            ma.transacciones AS transacciones_mes_actual,
            mp.total_ventas AS ventas_mes_anterior,
            mp.transacciones AS transacciones_mes_anterior,
            (ma.total_ventas - mp.total_ventas) AS diferencia_ventas,
            CASE 
                WHEN mp.total_ventas > 0 THEN
                    ROUND(((ma.total_ventas - mp.total_ventas) / mp.total_ventas) * 100, 2)
                ELSE 0
            END AS porcentaje_cambio
        FROM ventas_mes_actual ma, ventas_mes_anterior mp;
        """
        
        try:
            df = self.ejecutar_query(query)
            
            if df.empty:
                return {
                    'ventas_mes_actual': 0,
                    'ventas_mes_anterior': 0,
                    'transacciones_mes_actual': 0,
                    'transacciones_mes_anterior': 0,
                    'diferencia_ventas': 0,
                    'porcentaje_cambio': 0,
                    'tendencia': 'sin_datos'
                }
            
            row = df.iloc[0]
            porcentaje = float(row['porcentaje_cambio'])
            
            # Determinar tendencia
            if porcentaje > 5:
                tendencia = 'crecimiento'
            elif porcentaje < -5:
                tendencia = 'decrecimiento'
            else:
                tendencia = 'estable'
            
            resultado = {
                'ventas_mes_actual': float(row['ventas_mes_actual']),
                'ventas_mes_anterior': float(row['ventas_mes_anterior']),
                'transacciones_mes_actual': int(row['transacciones_mes_actual']),
                'transacciones_mes_anterior': int(row['transacciones_mes_anterior']),
                'diferencia_ventas': float(row['diferencia_ventas']),
                'porcentaje_cambio': porcentaje,
                'tendencia': tendencia
            }
            
            logger.info(f" Comparativa mensual: {porcentaje:+.2f}% ({tendencia})")
            return resultado
            
        except Exception as e:
            logger.warning(f"  Error obteniendo comparativa de ventas: {e}")
            return {
                'ventas_mes_actual': 0,
                'ventas_mes_anterior': 0,
                'transacciones_mes_actual': 0,
                'transacciones_mes_anterior': 0,
                'diferencia_ventas': 0,
                'porcentaje_cambio': 0,
                'tendencia': 'error'
            }
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info(" Conexión cerrada")
    
    # Nota: No usar __del__ porque causa problemas con FastAPI
    # La conexión se mantendrá abierta durante toda la vida de la aplicación


# =============================================================================
# FUNCIÓN DE PRUEBA
# =============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("  PROBANDO CONEXIÓN A BASE DE DATOS")
    print("=" * 80)
    
    try:
        db = PetStoreDatabase()
        
        print("\n Estadísticas Generales:")
        stats = db.obtener_estadisticas_generales()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
        
        print("\n Tipos de Mascotas:")
        df_mascotas = db.obtener_tipos_mascota_mas_comunes()
        print(df_mascotas.to_string(index=False))
        
        print("\n Días con Más Atención:")
        df_dias = db.obtener_dias_con_mas_atencion()
        print(df_dias.to_string(index=False))
        
        print("\n Conexión y consultas exitosas!")
        
    except Exception as e:
        print(f"\n Error: {e}")
    
    finally:
        print("\n" + "=" * 80)

