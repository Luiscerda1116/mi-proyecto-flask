from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
from models.Producto import Producto
import os

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')

    # Ruta para mostrar todos los productos
    @app.route('/productos')
    def listar_productos():
        productos = Producto.obtener_todos()
        return render_template('productos/listar.html', productos=productos)

    # Ruta para mostrar el formulario de crear producto
    @app.route('/crear')
    def mostrar_crear():
        return render_template('productos/crear.html')

    # Ruta para procesar la creación de producto
    @app.route('/crear', methods=['POST'])
    def crear_producto():
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            # Validaciones
            if not nombre:
                flash('El nombre del producto es obligatorio', 'error')
                return render_template('productos/crear.html')
            
            if precio <= 0:
                flash('El precio debe ser mayor a 0', 'error')
                return render_template('productos/crear.html')
            
            if stock < 0:
                flash('El stock no puede ser negativo', 'error')
                return render_template('productos/crear.html')
            
            # Crear producto
            producto_id = Producto.crear_producto(nombre, precio, stock)
            
            if producto_id:
                flash('Producto creado exitosamente', 'success')
                return redirect(url_for('listar_productos'))
            else:
                flash('Error al crear el producto', 'error')
                return render_template('productos/crear.html')
                
        except ValueError:
            flash('Por favor, ingresa valores válidos', 'error')
            return render_template('productos/crear.html')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            return render_template('productos/crear.html')

    # Ruta para mostrar el formulario de editar producto
    @app.route('/editar/<int:id>')
    def mostrar_editar(id):
        producto = Producto.obtener_por_id(id)
        if not producto:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('listar_productos'))
        return render_template('productos/editar.html', producto=producto)

    # Ruta para procesar la actualización de producto
    @app.route('/editar/<int:id>', methods=['POST'])
    def editar_producto(id):
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            # Validaciones
            if not nombre:
                flash('El nombre del producto es obligatorio', 'error')
                producto = Producto.obtener_por_id(id)
                return render_template('productos/editar.html', producto=producto)
            
            if precio <= 0:
                flash('El precio debe ser mayor a 0', 'error')
                producto = Producto.obtener_por_id(id)
                return render_template('productos/editar.html', producto=producto)
            
            if stock < 0:
                flash('El stock no puede ser negativo', 'error')
                producto = Producto.obtener_por_id(id)
                return render_template('productos/editar.html', producto=producto)
            
            # Actualizar producto
            if Producto.actualizar_producto(id, nombre, precio, stock):
                flash('Producto actualizado exitosamente', 'success')
                return redirect(url_for('listar_productos'))
            else:
                flash('Error al actualizar el producto', 'error')
                producto = Producto.obtener_por_id(id)
                return render_template('productos/editar.html', producto=producto)
                
        except ValueError:
            flash('Por favor, ingresa valores válidos', 'error')
            producto = Producto.obtener_por_id(id)
            return render_template('productos/editar.html', producto=producto)
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            producto = Producto.obtener_por_id(id)
            return render_template('productos/editar.html', producto=producto)

    # Ruta para eliminar producto
    @app.route('/eliminar/<int:id>')
    def confirmar_eliminar(id):
        producto = Producto.obtener_por_id(id)
        if not producto:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('listar_productos'))
        return render_template('productos/eliminar.html', producto=producto)

    # Ruta para procesar la eliminación de producto
    @app.route('/eliminar/<int:id>', methods=['POST'])
    def eliminar_producto(id):
        try:
            if Producto.eliminar_producto(id):
                flash('Producto eliminado exitosamente', 'success')
            else:
                flash('Error al eliminar el producto', 'error')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
        
        return redirect(url_for('listar_productos'))

    # Ruta API para obtener producto (opcional, para AJAX)
    @app.route('/api/producto/<int:id>')
    def api_obtener_producto(id):
        producto = Producto.obtener_por_id(id)
        if producto:
            return jsonify(producto)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404

    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)