from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos SQLite (en el directorio raíz)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo de base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'mensaje': self.mensaje,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form.get('mensaje', '')
    
    # Crear directorio datos si no existe
    os.makedirs('datos', exist_ok=True)
    
    # Guardar en archivo TXT
    guardar_txt(nombre, email, mensaje)
    
    # Guardar en archivo JSON
    guardar_json(nombre, email, mensaje)
    
    # Guardar en archivo CSV
    guardar_csv(nombre, email, mensaje)
    
    # Guardar en SQLite
    guardar_sqlite(nombre, email, mensaje)
    
    return render_template('resultado.html', nombre=nombre, email=email, mensaje=mensaje)

# Funciones para manejar archivos TXT
def guardar_txt(nombre, email, mensaje):
    with open('datos/datos.txt', 'a', encoding='utf-8') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Fecha: {timestamp}\n")
        file.write(f"Nombre: {nombre}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Mensaje: {mensaje}\n")
        file.write("-" * 50 + "\n")

@app.route('/datos_txt')
def mostrar_datos_txt():
    try:
        with open('datos/datos.txt', 'r', encoding='utf-8') as file:
            contenido = file.read()
        return f"<pre>{contenido}</pre>"
    except FileNotFoundError:
        return "No se encontraron datos en archivo TXT"

# Funciones para manejar archivos JSON
def guardar_json(nombre, email, mensaje):
    datos = {
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'nombre': nombre,
        'email': email,
        'mensaje': mensaje
    }
    
    # Leer datos existentes
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as file:
            lista_datos = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        lista_datos = []
    
    # Agregar nuevos datos
    lista_datos.append(datos)
    
    # Guardar datos actualizados
    with open('datos/datos.json', 'w', encoding='utf-8') as file:
        json.dump(lista_datos, file, indent=2, ensure_ascii=False)

@app.route('/datos_json')
def mostrar_datos_json():
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as file:
            datos = json.load(file)
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({"error": "No se encontraron datos en archivo JSON"})

# Funciones para manejar archivos CSV
def guardar_csv(nombre, email, mensaje):
    archivo_existe = os.path.exists('datos/datos.csv')
    
    with open('datos/datos.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Escribir encabezados si el archivo es nuevo
        if not archivo_existe:
            writer.writerow(['Fecha', 'Nombre', 'Email', 'Mensaje'])
        
        # Escribir datos
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([timestamp, nombre, email, mensaje])

@app.route('/datos_csv')
def mostrar_datos_csv():
    try:
        datos = []
        with open('datos/datos.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                datos.append(row)
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({"error": "No se encontraron datos en archivo CSV"})

# Funciones para manejar SQLite
def guardar_sqlite(nombre, email, mensaje):
    try:
        nuevo_usuario = Usuario(nombre=nombre, email=email, mensaje=mensaje)
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar en SQLite: {e}")

@app.route('/datos_sqlite')
def mostrar_datos_sqlite():
    try:
        usuarios = Usuario.query.all()
        datos = [usuario.to_dict() for usuario in usuarios]
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": f"Error al acceder a la base de datos: {str(e)}"})

@app.route('/usuarios')
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        return render_template('usuarios.html', usuarios=usuarios)
    except Exception as e:
        return f"Error al acceder a la base de datos: {str(e)}"

@app.route('/usuario/<int:id>')
def mostrar_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        return render_template('usuario_detalle.html', usuario=usuario)
    except Exception as e:
        return f"Error al acceder a la base de datos: {str(e)}"

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    except Exception as e:
        db.session.rollback()
        return f"Error al eliminar usuario: {str(e)}"

if __name__ == '__main__':
    # Crear las tablas al iniciar la aplicación (dentro del contexto de la app)
    with app.app_context():
        try:
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
    
    print("🚀 Iniciando aplicación Flask...")
    app.run(debug=True)