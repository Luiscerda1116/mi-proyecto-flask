from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sys
import os

# Agregar la carpeta Conexion al path para importar el módulo
sys.path.append(os.path.join(os.path.dirname(__file__), 'Conexion'))

try:
    from conexion import db
except ImportError:
    print("Error: No se pudo importar el módulo de conexión")
    db = None

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia por una clave segura

# Ruta principal
@app.route('/')
def index():
    """Página principal del proyecto"""
    return render_template('index.html')

# Ruta para probar la conexión a MySQL (requerida por la tarea)
@app.route('/test_db')
def test_database():
    """Prueba la conexión con MySQL"""
    if db is None:
        return "Error: Módulo de conexión no disponible"
    
    result = db.test_connection()
    return f"<h1>Prueba de Conexión MySQL</h1><p>{result}</p>"

# Rutas para gestión de usuarios
@app.route('/usuarios')
def listar_usuarios():
    """Muestra todos los usuarios"""
    if db is None:
        return "Error: Base de datos no disponible"
    
    usuarios = db.fetch_query("SELECT * FROM usuarios WHERE activo = TRUE ORDER BY fecha_registro DESC")
    
    if usuarios is None:
        flash('Error al obtener usuarios', 'error')
        return redirect(url_for('index'))
    
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        
        if not nombre or not email:
            flash('Nombre y email son obligatorios', 'error')
            return render_template('nuevo_usuario.html')
        
        # Insertar usuario en la base de datos
        query = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
        if db.execute_query(query, (nombre, email)):
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('listar_usuarios'))
        else:
            flash('Error al crear usuario', 'error')
    
    return render_template('nuevo_usuario.html')

# Rutas para productos (ejemplo adicional)
@app.route('/productos')
def listar_productos():
    """Muestra todos los productos con sus categorías"""
    if db is None:
        return "Error: Base de datos no disponible"
    
    query = """
    SELECT p.*, c.nombre_categoria 
    FROM productos p 
    LEFT JOIN categorias c ON p.id_categoria = c.id_categoria 
    ORDER BY p.fecha_creacion DESC
    """
    productos = db.fetch_query(query)
    
    if productos is None:
        flash('Error al obtener productos', 'error')
        return redirect(url_for('index'))
    
    return render_template('productos.html', productos=productos)

# API endpoints
@app.route('/api/usuarios')
def api_usuarios():
    """API para obtener usuarios en formato JSON"""
    usuarios = db.fetch_query("SELECT id_usuario, nombre, email FROM usuarios WHERE activo = TRUE")
    return jsonify(usuarios if usuarios else [])

@app.route('/api/productos')
def api_productos():
    """API para obtener productos en formato JSON"""
    productos = db.fetch_query("SELECT * FROM productos")
    return jsonify(productos if productos else [])

# Ruta para estadísticas
@app.route('/estadisticas')
def estadisticas():
    """Muestra estadísticas del sistema"""
    if db is None:
        return "Error: Base de datos no disponible"
    
    stats = {}
    
    # Contar usuarios
    result = db.fetch_query("SELECT COUNT(*) as total FROM usuarios WHERE activo = TRUE")
    stats['usuarios'] = result[0]['total'] if result else 0
    
    # Contar productos
    result = db.fetch_query("SELECT COUNT(*) as total FROM productos")
    stats['productos'] = result[0]['total'] if result else 0
    
    # Contar categorías
    result = db.fetch_query("SELECT COUNT(*) as total FROM categorias")
    stats['categorias'] = result[0]['total'] if result else 0
    
    return render_template('estadisticas.html', stats=stats)

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Iniciando aplicación Flask con MySQL...")
    print("Rutas disponibles:")
    print("- http://localhost:5000/ (Página principal)")
    print("- http://localhost:5000/test_db (Prueba de conexión)")
    print("- http://localhost:5000/usuarios (Lista de usuarios)")
    print("- http://localhost:5000/productos (Lista de productos)")
    print("- http://localhost:5000/estadisticas (Estadísticas)")
    
    app.run(debug=True, port=5000)