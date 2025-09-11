import mysql.connector
from mysql.connector import Error
import sys
import traceback

class MySQL:
    def __init__(self):
        """Inicializa la configuración de la base de datos"""
        self.config = {
            'host': 'localhost',
            'database': 'myslq',
            'user': 'root',
            'password': '',  # Tu contraseña
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }
        self.connection = None
        self.cursor = None

    def test_connection(self):
        """Prueba la conexión y devuelve un mensaje de estado"""
        try:
            # Intentar conectar
            connection = mysql.connector.connect(**self.config)
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                
                cursor.close()
                connection.close()
                
                return f"✅ Conexión exitosa. Versión de MySQL: {version[0]}"
            else:
                return "❌ No se pudo establecer la conexión"
                
        except mysql.connector.Error as e:
            return f"❌ Error de MySQL: {e}"
        except Exception as e:
            return f"❌ Error inesperado: {e}"

    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                self.cursor = self.connection.cursor()
            return True
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return False

    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
        except Error as e:
            print(f"Error al desconectar: {e}")

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        try:
            if not self.conectar():
                return None
            
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            
            resultados = self.cursor.fetchall()
            return resultados
            
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def ejecutar_insercion(self, consulta, parametros=None):
        """Ejecuta una consulta INSERT, UPDATE o DELETE"""
        try:
            if not self.conectar():
                return False
            
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error al ejecutar inserción: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def crear_tabla_usuarios(self):
        """Crea la tabla usuarios si no existe"""
        consulta = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        return self.ejecutar_insercion(consulta)

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos"""
        consulta = "SELECT id_usuario, nombre, email, fecha_creacion FROM usuarios ORDER BY fecha_creacion DESC"
        return self.ejecutar_consulta(consulta)

    def insertar_usuario(self, nombre, email):
        """Inserta un nuevo usuario en la base de datos"""
        consulta = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
        parametros = (nombre, email)
        return self.ejecutar_insercion(consulta, parametros)

# Instancia global para usar en Flask
db = MySQL()

# Verificación al importar
if __name__ == "__main__":
    print("🔧 Probando conexión a MySQL...")
    resultado = db.test_connection()
    print(resultado)
    
    print("\n📊 Creando tabla usuarios...")
    if db.crear_tabla_usuarios():
        print("✅ Tabla usuarios creada/verificada correctamente")
    else:
        print("❌ Error al crear la tabla usuarios")