# Sistema de Gestión de Productos - Flask

Sistema CRUD completo desarrollado en Flask para la gestión de productos con interfaz web moderna.

## Características

- ✅ **CRUD Completo**: Crear, Leer, Actualizar, Eliminar productos
- ✅ **Base de datos**: SQLite integrada
- ✅ **Interfaz moderna**: Bootstrap 5 con diseño responsivo
- ✅ **Validaciones**: Frontend y Backend
- ✅ **Mensajes Flash**: Feedback visual para el usuario
- ✅ **Manejo de errores**: Páginas personalizadas 404 y 500

## Tecnologías utilizadas

- **Backend**: Python 3.x, Flask
- **Base de datos**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Plantillas**: Jinja2

## Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

## Estructura del proyecto

```
mi_proyecto_flask/
├── app.py                 # Aplicación principal Flask
├── config.py             # Configuración de la aplicación
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Documentación
├── .gitignore           # Archivos ignorados por Git
├── .env.example         # Ejemplo de variables de entorno
├── models/              # Modelos de datos
│   ├── __init__.py
│   └── Producto.py      # Modelo Producto
└── templates/           # Plantillas HTML
    ├── base.html        # Plantilla base
    ├── index.html       # Página principal
    ├── productos/       # Plantillas de productos
    │   ├── crear.html   # Crear producto
    │   ├── listar.html  # Listar productos
    │   ├── editar.html  # Editar producto
    │   └── eliminar.html # Eliminar producto
    └── errors/          # Páginas de error
        ├── 404.html     # Error 404
        └── 500.html     # Error 500
```

## Funcionalidades

### Gestión de Productos
- **Crear**: Formulario para agregar nuevos productos
- **Listar**: Tabla con todos los productos y estado del stock
- **Editar**: Modificar información de productos existentes
- **Eliminar**: Eliminar productos con confirmación

### Características adicionales
- Validación de datos en frontend y backend
- Indicadores visuales de stock (disponible, poco stock, agotado)
- Interfaz responsiva para móviles y desktop
- Mensajes de confirmación y error
- Navegación intuitiva

## Base de datos

La aplicación utiliza SQLite con la siguiente estructura:

```sql
CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Desarrollo

### Ejecutar en modo desarrollo
```bash
flask run --debug
```

### Ejecutar pruebas
```bash
python test_db.py
```

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autor

[Tu Nombre] - [tu-email@ejemplo.com]

## Capturas de pantalla

### Página Principal
Interface moderna con navegación clara y acceso rápido a funcionalidades.

### Lista de Productos
Tabla responsiva con indicadores de stock y acciones disponibles.

### Formularios
Validación en tiempo real y feedback visual para el usuario.