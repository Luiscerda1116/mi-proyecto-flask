import sqlite3
import os

class Producto:
    def __init__(self, id_producto=None, nombre=None, precio=None, stock=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @staticmethod
    def get_db_path():
        """Obtener la ruta de la base de datos SQLite"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'desarrollo_web.db')

    @staticmethod
    def init_db():
        """Inicializar la base de datos y crear la tabla si no existe"""
        db_path = Producto.get_db_path()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Crear tabla productos si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        connection.commit()
        connection.close()

    @staticmethod
    def get_db_connection():
        """Crear conexión a la base de datos SQLite"""
        try:
            Producto.init_db()  # Asegurar que la DB existe
            db_path = Producto.get_db_path()
            connection = sqlite3.connect(db_path)
            connection.row_factory = sqlite3.Row  # Para obtener resultados como diccionario
            return connection
        except Exception as err:
            print(f"Error connecting to SQLite: {err}")
            return None

    @classmethod
    def crear_producto(cls, nombre, precio, stock):
        """Crear un nuevo producto"""
        connection = cls.get_db_connection()
        if not connection:
            print("No se pudo conectar a la base de datos")
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", 
                         (nombre, precio, stock))
            connection.commit()
            producto_id = cursor.lastrowid
            print(f"Producto creado exitosamente con ID: {producto_id}")
            return producto_id
        except Exception as err:
            print(f"Error creating product: {err}")
            return False
        finally:
            connection.close()

    @classmethod
    def obtener_todos(cls):
        """Obtener todos los productos"""
        connection = cls.get_db_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC")
            productos = [dict(row) for row in cursor.fetchall()]
            return productos
        except Exception as err:
            print(f"Error fetching products: {err}")
            return []
        finally:
            connection.close()

    @classmethod
    def obtener_por_id(cls, id_producto):
        """Obtener un producto por su ID"""
        connection = cls.get_db_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as err:
            print(f"Error fetching product: {err}")
            return None
        finally:
            connection.close()

    @classmethod
    def actualizar_producto(cls, id_producto, nombre, precio, stock):
        """Actualizar un producto existente"""
        connection = cls.get_db_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE productos 
                            SET nombre = ?, precio = ?, stock = ? 
                            WHERE id_producto = ?""", 
                         (nombre, precio, stock, id_producto))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as err:
            print(f"Error updating product: {err}")
            return False
        finally:
            connection.close()

    @classmethod
    def eliminar_producto(cls, id_producto):
        """Eliminar un producto"""
        connection = cls.get_db_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as err:
            print(f"Error deleting product: {err}")
            return False
        finally:
            connection.close()

    def to_dict(self):
        """Convertir el objeto a diccionario"""
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }