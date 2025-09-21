import mysql.connector
from mysql.connector import Error

# Configuración con tu contraseña
config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'desarrollo_web',
    'port': 3306
}

def test_connection():
    try:
        print("🔄 Intentando conectar a MySQL...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ ¡Conexión exitosa a MySQL!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            
            print(f"📊 Usuarios encontrados: {len(usuarios)}")
            for usuario in usuarios:
                print(f"   - {usuario[1]} ({usuario[2]})")
            
            cursor.close()
            connection.close()
            print("🔒 Conexión cerrada correctamente")
            return True
            
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verificar que MySQL esté ejecutándose")
        print("2. Revisar la contraseña")
        print("3. Verificar que la base de datos 'desarrollo_web' exista")
        return False

if __name__ == "__main__":
    print("🧪 Probando conexión a MySQL...")
    test_connection()