# Configuración de Base de Datos

## Requisitos:
- MySQL 5.7 o superior
- Usuario root con contraseña 'admin' (o modificar en conectar.py)

## Instalación:

### Opción 1: Usando phpMyAdmin
1. Abrir `localhost/phpmyadmin`
2. Clic en "Importar"
3. Seleccionar archivo `database.sql`
4. Clic en "Continuar"

### Opción 2: Desde línea de comandos
```bash
mysql -u root -padmin < database.sql
```

### Opción 3: Desde MySQL Command Line
```sql
mysql -u root -padmin
source /ruta/completa/database.sql
```

## Estructura de la Base de Datos:

### Tabla: usuarios
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `nombre` (VARCHAR 100, NOT NULL)
- `email` (VARCHAR 150, UNIQUE, NOT NULL)
- `edad` (INT)
- `fecha_registro` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `activo` (BOOLEAN, DEFAULT TRUE)

### Tabla: categorias
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `nombre` (VARCHAR 100, NOT NULL)
- `descripcion` (TEXT)
- `fecha_creacion` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Tabla: usuario_categoria
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `usuario_id` (INT, FOREIGN KEY)
- `categoria_id` (INT, FOREIGN KEY)
- `fecha_asignacion` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## Datos de Ejemplo:
El script incluye 5 usuarios de prueba y 3 categorías con sus respectivas relaciones.

## Configuración de Conexión:
Archivo: `Conexion/conectar.py`
```python
'host': 'localhost',
'database': 'prueba_flask',
'user': 'root',
'password': 'admin'
```

## Solución de Problemas:

### Error: "Access denied"
- Verificar que la contraseña sea 'admin'
- O cambiar la contraseña en `conectar.py`

### Error: "Database doesn't exist"
- Ejecutar el script `database.sql` primero

### Error: "Table doesn't exist"
- Verificar que todas las tablas se crearon correctamente
- Ejecutar: `SHOW TABLES;` en MySQL