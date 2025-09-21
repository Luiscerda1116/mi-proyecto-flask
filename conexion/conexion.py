import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establecer conexión con la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='mi_proyecto_flask',
                user='root',
                password=''  # Cambia aquí por tu contraseña de MySQL
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return False

    def execute_query(self, query, params=None):
        """Ejecutar una consulta SELECT"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def execute_insert(self, query, params=None):
        """Ejecutar una consulta INSERT, UPDATE o DELETE"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error al ejecutar inserción: {e}")
            self.connection.rollback()
            return 0

    def close(self):
        """Cerrar la conexión"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

# Función helper para obtener una conexión
def get_db_connection():
    db = DatabaseConnection()
    if db.connect():
        return db
    return None