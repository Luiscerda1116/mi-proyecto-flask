CREATE DATABASE IF NOT EXISTS desarrollo_web;
USE desarrollo_web;

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop Dell', 1299.99, 15),
('Mouse Gamer', 99.99, 50);