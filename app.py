from flask import Flask, render_template

# Crear la instancia de Flask
app = Flask(__name__)

# Ruta principal (página de inicio)
@app.route('/')
def index():
    # Datos dinámicos para la plantilla
    user_name = "Estudiante"
    projects = [
        {"name": "Proyecto 1", "description": "Sistema de gestión de tareas"},
        {"name": "Proyecto 2", "description": "API REST con Flask"},
        {"name": "Proyecto 3", "description": "Aplicación web con base de datos"}
    ]
    return render_template('index.html', 
                         user_name=user_name, 
                         projects=projects)

# Ruta "Acerca de"
@app.route('/about')
def about():
    # Información del desarrollador
    developer_info = {
        "name": "Tu Nombre",
        "university": "Tu Universidad", 
        "career": "Tu Carrera",
        "skills": ["Python", "Flask", "HTML", "CSS", "JavaScript", "Git"]
    }
    return render_template('about.html', developer=developer_info)

# Manejo de errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Configuración para ejecutar la aplicación
if __name__ == '__main__':
    import os
    # Configuración para Render y desarrollo local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # ← Cambiar a debug=False