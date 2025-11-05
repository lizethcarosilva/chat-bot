-- ============================================================================
-- SCRIPT PARA CREAR TABLAS DE PRODUCTOS Y VENTAS
-- Pet Store - Sistema de Inventario y Ventas
-- ============================================================================

-- TABLA: producto
-- Gestiona el inventario de productos para mascotas
-- ============================================================================
CREATE TABLE IF NOT EXISTS producto (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),  -- Ej: Alimento, Juguetes, Medicamentos, Accesorios
    codigo_barras VARCHAR(50) UNIQUE,
    
    -- Precios
    precio_compra DECIMAL(10, 2) NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    margen_ganancia DECIMAL(5, 2),  -- Porcentaje de ganancia
    
    -- Inventario
    stock_actual INTEGER NOT NULL DEFAULT 0,
    stock_minimo INTEGER NOT NULL DEFAULT 10,
    stock_maximo INTEGER NOT NULL DEFAULT 100,
    
    -- Fechas y vencimiento
    fecha_vencimiento DATE,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lote VARCHAR(50),
    
    -- Proveedor
    proveedor VARCHAR(200),
    telefono_proveedor VARCHAR(20),
    
    -- Información adicional
    peso_kg DECIMAL(8, 2),
    unidad_medida VARCHAR(20),  -- Ej: kg, unidad, litro
    
    -- Control
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_producto_categoria ON producto(categoria);
CREATE INDEX idx_producto_stock ON producto(stock_actual);
CREATE INDEX idx_producto_vencimiento ON producto(fecha_vencimiento);
CREATE INDEX idx_producto_activo ON producto(activo);


-- ============================================================================
-- TABLA: venta
-- Registra las ventas realizadas
-- ============================================================================
CREATE TABLE IF NOT EXISTS venta (
    venta_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(client_id),
    
    -- Fecha y hora de la venta
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Montos
    subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
    descuento DECIMAL(10, 2) DEFAULT 0,
    impuesto DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    
    -- Método de pago
    metodo_pago VARCHAR(50),  -- Ej: Efectivo, Tarjeta, Transferencia
    estado VARCHAR(50) DEFAULT 'COMPLETADA',  -- COMPLETADA, CANCELADA, PENDIENTE
    
    -- Usuario que realizó la venta
    user_id INTEGER REFERENCES "user"(user_id),
    
    -- Observaciones
    observaciones TEXT,
    
    -- Control
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_venta_fecha ON venta(fecha_venta);
CREATE INDEX idx_venta_cliente ON venta(client_id);
CREATE INDEX idx_venta_estado ON venta(estado);


-- ============================================================================
-- TABLA: detalle_venta
-- Detalle de productos vendidos en cada venta
-- ============================================================================
CREATE TABLE IF NOT EXISTS detalle_venta (
    detalle_id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES venta(venta_id) ON DELETE CASCADE,
    producto_id INTEGER REFERENCES producto(producto_id),
    
    -- Cantidad y precios
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(10, 2) DEFAULT 0,
    
    -- Control
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_detalle_venta ON detalle_venta(venta_id);
CREATE INDEX idx_detalle_producto ON detalle_venta(producto_id);


-- ============================================================================
-- TRIGGER: Actualizar stock al registrar venta
-- ============================================================================
CREATE OR REPLACE FUNCTION actualizar_stock_venta()
RETURNS TRIGGER AS $$
BEGIN
    -- Restar del stock cuando se inserta un detalle de venta
    IF (TG_OP = 'INSERT') THEN
        UPDATE producto
        SET stock_actual = stock_actual - NEW.cantidad,
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE producto_id = NEW.producto_id;
    END IF;
    
    -- Si se cancela una venta, devolver el stock
    IF (TG_OP = 'DELETE') THEN
        UPDATE producto
        SET stock_actual = stock_actual + OLD.cantidad,
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE producto_id = OLD.producto_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_stock
AFTER INSERT OR DELETE ON detalle_venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_venta();


-- ============================================================================
-- TRIGGER: Calcular totales de venta automáticamente
-- ============================================================================
CREATE OR REPLACE FUNCTION calcular_total_venta()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE venta
    SET 
        subtotal = (
            SELECT COALESCE(SUM(subtotal), 0)
            FROM detalle_venta
            WHERE venta_id = NEW.venta_id
        ),
        total = (
            SELECT COALESCE(SUM(subtotal), 0) - COALESCE(descuento, 0) + COALESCE(impuesto, 0)
            FROM detalle_venta
            WHERE venta_id = NEW.venta_id
        )
    WHERE venta_id = NEW.venta_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calcular_total
AFTER INSERT OR UPDATE OR DELETE ON detalle_venta
FOR EACH ROW
EXECUTE FUNCTION calcular_total_venta();


-- ============================================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================================

-- Insertar categorías de productos comunes
INSERT INTO producto (nombre, descripcion, categoria, precio_compra, precio_venta, stock_actual, stock_minimo, stock_maximo, proveedor, fecha_vencimiento)
VALUES
    ('Alimento Premium Perro Adulto 15kg', 'Alimento balanceado para perros adultos', 'Alimento', 45.00, 65.00, 50, 10, 100, 'PetFood Supply', '2025-06-30'),
    ('Alimento Gato Cachorro 3kg', 'Alimento especial para gatitos', 'Alimento', 18.00, 28.00, 30, 10, 80, 'PetFood Supply', '2025-05-15'),
    ('Collar Antipulgas Grande', 'Collar antipulgas para perros grandes', 'Medicamentos', 12.00, 22.00, 25, 5, 50, 'VetMed Inc', '2025-12-31'),
    ('Juguete Pelota Goma', 'Pelota de goma para perros', 'Juguetes', 3.00, 7.50, 100, 20, 200, 'PetToys Co', NULL),
    ('Shampoo Hipoalergénico 500ml', 'Shampoo para mascotas con piel sensible', 'Higiene', 8.00, 15.00, 40, 10, 80, 'PetCare Products', '2025-08-20'),
    ('Correa Retráctil 5m', 'Correa extensible para paseos', 'Accesorios', 10.00, 18.00, 35, 10, 60, 'PetAccess Ltd', NULL),
    ('Arena Sanitaria 10kg', 'Arena para gatos aglutinante', 'Higiene', 7.00, 13.00, 60, 15, 100, 'CleanPet', NULL),
    ('Vitaminas Multivitamínico', 'Suplemento vitamínico para mascotas', 'Medicamentos', 15.00, 28.00, 20, 5, 40, 'VetMed Inc', '2025-11-30'),
    ('Cama Ortopédica Mediana', 'Cama con soporte ortopédico', 'Accesorios', 35.00, 65.00, 15, 5, 30, 'PetComfort', NULL),
    ('Snacks Dentales 250g', 'Premios para limpieza dental', 'Alimento', 5.00, 10.00, 80, 20, 150, 'PetFood Supply', '2025-07-15')
ON CONFLICT DO NOTHING;


-- Ejemplo de venta (descomentar si quieres probar)
/*
-- Crear una venta de ejemplo
INSERT INTO venta (client_id, fecha_venta, metodo_pago, descuento, impuesto, user_id)
VALUES (1, CURRENT_TIMESTAMP, 'Efectivo', 0, 0, 1)
RETURNING venta_id;

-- Agregar productos a la venta (reemplaza <venta_id> con el ID retornado arriba)
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
VALUES
    (<venta_id>, 1, 2, 65.00, 130.00),  -- 2 bolsas de alimento
    (<venta_id>, 4, 3, 7.50, 22.50);     -- 3 juguetes
*/


-- ============================================================================
-- VISTAS ÚTILES PARA REPORTES
-- ============================================================================

-- Vista: Productos con bajo inventario
CREATE OR REPLACE VIEW vista_bajo_inventario AS
SELECT 
    p.producto_id,
    p.nombre,
    p.categoria,
    p.stock_actual,
    p.stock_minimo,
    (p.stock_minimo - p.stock_actual) AS unidades_faltantes,
    p.precio_compra,
    ((p.stock_minimo - p.stock_actual) * p.precio_compra) AS costo_reposicion
FROM producto p
WHERE p.stock_actual < p.stock_minimo
  AND p.activo = true
ORDER BY p.stock_actual ASC;


-- Vista: Productos próximos a vencer
CREATE OR REPLACE VIEW vista_productos_por_vencer AS
SELECT 
    p.producto_id,
    p.nombre,
    p.categoria,
    p.fecha_vencimiento,
    p.stock_actual,
    (DATE(p.fecha_vencimiento) - CURRENT_DATE) AS dias_hasta_vencer,
    (p.stock_actual * p.precio_venta) AS valor_inventario
FROM producto p
WHERE p.fecha_vencimiento IS NOT NULL
  AND p.fecha_vencimiento BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
  AND p.activo = true
  AND p.stock_actual > 0
ORDER BY p.fecha_vencimiento ASC;


-- Vista: Ventas del día
CREATE OR REPLACE VIEW vista_ventas_dia AS
SELECT 
    v.venta_id,
    v.fecha_venta,
    c.name AS cliente,
    v.total,
    v.metodo_pago,
    u.name AS vendedor
FROM venta v
JOIN client c ON v.client_id = c.client_id
LEFT JOIN "user" u ON v.user_id = u.user_id
WHERE DATE(v.fecha_venta) = CURRENT_DATE
  AND v.activo = true
ORDER BY v.fecha_venta DESC;


-- ============================================================================
-- COMENTARIOS EN LAS TABLAS
-- ============================================================================
COMMENT ON TABLE producto IS 'Catálogo de productos para mascotas';
COMMENT ON TABLE venta IS 'Registro de ventas realizadas';
COMMENT ON TABLE detalle_venta IS 'Detalle de productos vendidos en cada venta';

COMMENT ON COLUMN producto.stock_minimo IS 'Stock mínimo antes de generar alerta';
COMMENT ON COLUMN producto.fecha_vencimiento IS 'Fecha de vencimiento del producto (si aplica)';
COMMENT ON COLUMN venta.metodo_pago IS 'Efectivo, Tarjeta, Transferencia, etc.';


-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================
SELECT 'Tablas creadas exitosamente' AS resultado;

-- Ver productos insertados
SELECT COUNT(*) AS total_productos FROM producto;

-- Ver estructura de las tablas
\d producto;
\d venta;
\d detalle_venta;

