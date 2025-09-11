-- Script de Base de Datos para Flask-MySQL Project
-- Autor: Luis Cerda
-- Fecha: Septiembre 2025

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS prueba_flask;
USE prueba_flask;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    edad INT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar datos de ejemplo
INSERT INTO usuarios (nombre, email, edad) VALUES
('Juan Pérez', 'juan.perez@email.com', 25),
('María García', 'maria.garcia@email.com', 30),
('Carlos López', 'carlos.lopez@email.com', 28),
('Ana Martínez', 'ana.martinez@email.com', 22),
('Luis Rodríguez', 'luis.rodriguez@email.com', 35);

-- Crear tabla de categorías (si la usas)
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar categorías de ejemplo
INSERT INTO categorias (nombre, descripcion) VALUES
('Administradores', 'Usuarios con permisos administrativos'),
('Usuarios Regulares', 'Usuarios con permisos básicos'),
('Invitados', 'Usuarios con acceso limitado');

-- Crear tabla de relación usuario-categoría (si la usas)
CREATE TABLE IF NOT EXISTS usuario_categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    categoria_id INT,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

-- Asignar categorías a usuarios
INSERT INTO usuario_categoria (usuario_id, categoria_id) VALUES
(1, 1), -- Juan es administrador
(2, 2), -- María es usuario regular
(3, 2), -- Carlos es usuario regular
(4, 3), -- Ana es invitada
(5, 1); -- Luis es administrador

-- Consultas útiles para verificar los datos
-- SELECT * FROM usuarios;
-- SELECT * FROM categorias;
-- SELECT u.nombre, c.nombre as categoria 
-- FROM usuarios u 
-- JOIN usuario_categoria uc ON u.id = uc.usuario_id 
-- JOIN categorias c ON uc.categoria_id = c.id;