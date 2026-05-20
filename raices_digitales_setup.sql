-- ============================================================
-- SCRIPT DE BASE DE DATOS - PROYECTO RAÍCES DIGITALES
-- DISEÑADO PARA EVITAR SESGOS Y PROVEER DATOS REALISTAS
-- ============================================================

CREATE DATABASE IF NOT EXISTS raices_digitales;
USE raices_digitales;

-- Limpieza de tablas existentes en orden de dependencia para evitar conflictos de claves foráneas
DROP TABLE IF EXISTS detalle_venta;
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS monitoreo_chinampa;
DROP TABLE IF EXISTS inventario;
DROP TABLE IF EXISTS cosecha;
DROP TABLE IF EXISTS terreno;
DROP TABLE IF EXISTS estudiante;
DROP TABLE IF EXISTS semilla;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS productor;
DROP TABLE IF EXISTS categoria;

-- 1. Tabla de Categorías de Semillas/Plantas
CREATE TABLE IF NOT EXISTS categoria (
    Id_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Categoria VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Tabla de Productores (Agricultores)
CREATE TABLE IF NOT EXISTS productor (
    Id_Productor INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Correo VARCHAR(255) NOT NULL UNIQUE,
    Telefono VARCHAR(20),
    Contrasena VARCHAR(255) NOT NULL,
    Fecha_Registro DATE DEFAULT (CURRENT_DATE),
    Tipo_Suelo VARCHAR(50) DEFAULT 'Suelo Franco',
    Filtro_Agua VARCHAR(100) DEFAULT 'Ninguno'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Tabla de Clientes (Compradores del Ecosistema)
CREATE TABLE IF NOT EXISTS cliente (
    Id_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Telefono VARCHAR(20),
    Correo VARCHAR(255) NOT NULL UNIQUE,
    Localidad VARCHAR(255),
    Contrasena VARCHAR(255) NOT NULL,
    Fecha_Registro DATE DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Tabla de Semillas en Catálogo (Especificaciones del Ecosistema)
CREATE TABLE IF NOT EXISTS semilla (
    Id_Semilla INT AUTO_INCREMENT PRIMARY KEY,
    Id_Categoria INT,
    Nombre_Semilla VARCHAR(255) NOT NULL,
    Valor FLOAT, -- Costo de inversión de la semilla
    Tiempo_Produccion INT, -- Días estimados
    pH_Optimo FLOAT,
    Temporada VARCHAR(50), -- Primavera-Verano, Otoño-Invierno, Perennes
    FOREIGN KEY (Id_Categoria) REFERENCES categoria(Id_Categoria) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Tabla de Estudiantes de Apoyo (Rol Social / Académico)
CREATE TABLE IF NOT EXISTS estudiante (
    Id_Estudiante INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Correo VARCHAR(255) NOT NULL UNIQUE,
    Contrasena VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Tabla de Terrenos (Chinampas)
CREATE TABLE IF NOT EXISTS terreno (
    Id_Terreno INT AUTO_INCREMENT PRIMARY KEY,
    Id_Productor INT NOT NULL,
    Id_Estudiante INT,
    FOREIGN KEY (Id_Productor) REFERENCES productor(Id_Productor) ON DELETE CASCADE,
    FOREIGN KEY (Id_Estudiante) REFERENCES estudiante(Id_Estudiante) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Tabla de Cosechas en Curso
CREATE TABLE IF NOT EXISTS cosecha (
    Id_Cosecha INT AUTO_INCREMENT PRIMARY KEY,
    Id_Productor INT NOT NULL,
    Id_Terreno INT NOT NULL,
    Id_Semilla INT NOT NULL,
    Temporada VARCHAR(100),
    Estatus VARCHAR(100) DEFAULT 'En proceso',
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Valor_Neto FLOAT,
    FOREIGN KEY (Id_Productor) REFERENCES productor(Id_Productor) ON DELETE CASCADE,
    FOREIGN KEY (Id_Terreno) REFERENCES terreno(Id_Terreno) ON DELETE CASCADE,
    FOREIGN KEY (Id_Semilla) REFERENCES semilla(Id_Semilla) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Tabla de Inventario de Cosechas (Stock Disponible)
CREATE TABLE IF NOT EXISTS inventario (
    Id_Inventario INT AUTO_INCREMENT PRIMARY KEY,
    Id_Productor INT NOT NULL,
    Id_Cosecha INT,
    Lote VARCHAR(100), -- Nombre de semilla o lote descriptivo
    Cantidad FLOAT NOT NULL, -- Hectáreas o cantidad de cosecha
    Unidad_Medida VARCHAR(50) DEFAULT 'Kg',
    Precio_Actual FLOAT NOT NULL, -- Precio de venta estimado en el mercado
    Observaciones TEXT,
    Estado VARCHAR(50) DEFAULT 'En Bodega',
    FOREIGN KEY (Id_Productor) REFERENCES productor(Id_Productor) ON DELETE CASCADE,
    FOREIGN KEY (Id_Cosecha) REFERENCES cosecha(Id_Cosecha) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Tabla de Monitoreo Semanal de Chinampas (Calidad Ambiental)
CREATE TABLE IF NOT EXISTS monitoreo_chinampa (
    Id_Monitoreo INT AUTO_INCREMENT PRIMARY KEY,
    Id_Estudiante INT NOT NULL,
    Id_Productor INT NOT NULL,
    Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    PH DECIMAL(4,2) NOT NULL,
    Salinidad DECIMAL(5,2) NOT NULL,
    Humedad DECIMAL(5,2) NOT NULL,
    Temperatura DECIMAL(5,2) NOT NULL,
    Observaciones TEXT,
    FOREIGN KEY (Id_Estudiante) REFERENCES estudiante(Id_Estudiante) ON DELETE CASCADE,
    FOREIGN KEY (Id_Productor) REFERENCES productor(Id_Productor) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Tabla de Ventas Generadas
CREATE TABLE IF NOT EXISTS venta (
    Id_Venta INT AUTO_INCREMENT PRIMARY KEY,
    Id_Cliente INT NOT NULL,
    Fecha_Venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    Total FLOAT NOT NULL,
    Metodo_Pago VARCHAR(50),
    Estatus VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (Id_Cliente) REFERENCES cliente(Id_Cliente) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Tabla de Detalles de Ventas
CREATE TABLE IF NOT EXISTS detalle_venta (
    Id_Detalle INT AUTO_INCREMENT PRIMARY KEY,
    Id_Venta INT NOT NULL,
    Id_Inventario INT NOT NULL,
    Cantidad FLOAT NOT NULL,
    Precio_Unitario FLOAT NOT NULL,
    FOREIGN KEY (Id_Venta) REFERENCES venta(Id_Venta) ON DELETE CASCADE,
    FOREIGN KEY (Id_Inventario) REFERENCES inventario(Id_Inventario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- INSERCIÓN DE DATOS SEMILLA (DATOS REALISTAS PARA EVITAR SESGOS)
-- ============================================================

-- A. Categorías básicas
INSERT INTO categoria (Nombre_Categoria) VALUES 
('Frutas'),
('Hortaliza de hoja'),
('Ornamental / Flor'),
('Granos'),
('Tubérculos');

-- B. Catálogo de Semillas de Xochimilco
-- Estructuradas con valores de mercado reales y pH óptimos específicos
INSERT INTO semilla (Id_Categoria, Nombre_Semilla, Valor, Tiempo_Produccion, pH_Optimo, Temporada) VALUES 
(1, 'Durazno', 290.0, 180, 6.5, 'Perennes'),
(2, 'Espinaca', 144.0, 45, 6.8, 'Primavera-Verano'),
(3, 'Zempoalxochitl', 62.5, 90, 7.0, 'Otoño-Invierno'),
(1, 'Aceituna', 320.0, 365, 7.25, 'Perennes'),
(2, 'Lechuga Romana', 85.0, 60, 6.5, 'Primavera-Verano'),
(4, 'Maíz Blanco', 120.0, 150, 6.8, 'Primavera-Verano'),
(5, 'Papa', 110.0, 120, 5.5, 'Otoño-Invierno'),
(3, 'Caléndula', 50.0, 75, 6.2, 'Otoño-Invierno');

-- C. Productores de prueba (Contraseñas con hash de pbkdf2:sha256/werkzeug equivalentes a '123456')
INSERT INTO productor (Nombre, Correo, Telefono, Contrasena, Tipo_Suelo, Filtro_Agua) VALUES 
('Ivan Fernandez Fernandez', 'ivan@unrc.edu.mx', '5512345678', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1', 'Suelo Franco Arcilloso', 'Ahuejote'),
('Josue Jair Pelagio Monroy', 'josue@unrc.edu.mx', '5587654321', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1', 'Suelo Limoso', 'Ahuehuete'),
('Mauricio Fernandez', 'mauricio@unrc.edu.mx', '5523456789', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1', 'Suelo Franco', 'Sauce llorón'),
('Axel Sanchez', 'axel@unrc.edu.mx', '5534567890', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1', 'Suelo Franco Arenoso', 'Ninguno'),
('Mateo Jurado Flores', 'mateo@unrc.edu.mx', '5545678901', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1', 'Suelo Franco', 'Fresnos');

-- D. Estudiantes registrados (Contraseñas equivalentes a '123456')
INSERT INTO estudiante (Nombre, Correo, Contrasena) VALUES 
('Ana Sofia Martinez', 'ana.sofia@uam.mx', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1'),
('Carlos Gomez Perez', 'carlos.g@urc.mx', 'pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1');

-- E. Terrenos iniciales
INSERT INTO terreno (Id_Productor, Id_Estudiante) VALUES 
(1, 1),
(1, 2),
(2, 2),
(3, 1),
(5, 2);

-- F. Cosechas registradas (algunas en proceso y otras listas para inventario)
INSERT INTO cosecha (Id_Productor, Id_Terreno, Id_Semilla, Temporada, Estatus, Fecha_Inicio, Fecha_Fin, Valor_Neto) VALUES 
(1, 1, 1, 'Perennes', 'Terminada', '2026-01-10', '2026-05-10', 145000.0),
(1, 2, 2, 'Primavera-Verano', 'Terminada', '2026-03-01', '2026-04-15', 65520.0),
(5, 5, 3, 'Otoño-Invierno', 'Terminada', '2025-10-01', '2026-01-15', 4187.5),
(3, 4, 6, 'Primavera-Verano', 'En proceso', '2026-04-01', NULL, NULL);

INSERT INTO inventario (Id_Productor, Id_Cosecha, Lote, Cantidad, Unidad_Medida, Precio_Actual, Observaciones, Estado) VALUES 
(1, 1, 'Lote Durazno Principal', 500.0, 'Kg', 145000.0, 'Excelente calidad, color uniforme', 'En Bodega'),
(1, 2, 'Lote Espinaca Tierna', 455.0, 'Manojo', 144.0, 'Recién cosechada, hojas frescas', 'En Bodega'),
(5, 3, 'Lote Zempoalxochitl (planta)', 67.0, 'Pieza', 62.5, 'Listas para venta de festividades', 'En Bodega');

-- H. Monitoreos Ambientales Iniciales (Chinampas)
INSERT INTO monitoreo_chinampa (Id_Estudiante, Id_Productor, PH, Salinidad, Humedad, Temperatura, Observaciones) VALUES 
(1, 1, 6.8, 1.2, 75.0, 22.5, 'El pH del suelo es óptimo para el durazno. Buena humedad de canal.'),
(1, 3, 7.2, 1.8, 65.5, 24.0, 'Salinidad ligeramente elevada, se sugerirá riego por goteo.'),
(2, 5, 5.8, 0.9, 80.0, 21.0, 'Tierra húmeda y pH levemente ácido, adecuado para flores ornamentales.');
