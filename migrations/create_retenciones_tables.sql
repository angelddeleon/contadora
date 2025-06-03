-- Drop the alembic_version table if it exists
DROP TABLE IF EXISTS alembic_version;

-- Eliminar las tablas si existen
DROP TABLE IF EXISTS retenciones_ventas;
DROP TABLE IF EXISTS retenciones_compras;

-- Tabla de retenciones de ventas
CREATE TABLE IF NOT EXISTS retenciones_ventas (
    id_retencion INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    idfacturaventa INT NOT NULL,
    numero_comprobante VARCHAR(50) NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,
    fecha_registro DATE NOT NULL,
    porcentaje_retencion FLOAT NOT NULL,
    valor_retencion DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (idfacturaventa) REFERENCES libro_ventas(idfacturaventa) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    INDEX idx_fecha_emision (fecha_emision),
    INDEX idx_fecha_registro (fecha_registro),
    INDEX idx_factura (idfacturaventa),
    INDEX idx_cliente (id_cliente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de retenciones de compras
CREATE TABLE IF NOT EXISTS retenciones_compras (
    id_retencion INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    idfacturacompra INT NOT NULL,
    numero_comprobante VARCHAR(50) NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,
    fecha_registro DATE NOT NULL,
    porcentaje_retencion FLOAT NOT NULL,
    valor_retencion DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (idfacturacompra) REFERENCES libro_compras(idfacturacompra) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    INDEX idx_fecha_emision (fecha_emision),
    INDEX idx_fecha_registro (fecha_registro),
    INDEX idx_factura (idfacturacompra),
    INDEX idx_cliente (id_cliente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 