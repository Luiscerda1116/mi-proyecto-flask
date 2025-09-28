import sqlite3
import os
from models.Producto import Producto

print("=== PRUEBA DE CONEXIÓN A SQLITE ===")
db_path = Producto.get_db_path()
print(f"Ruta de la base de datos: {db_path}")
print("-" * 50)

try:
    print("Inicializando base de datos...")
    Producto.init_db()
    print("✅ Base de datos inicializada!")
    
    print("Probando conexión...")
    connection = Producto.get_db_connection()
    if connection:
        print("✅ CONEXIÓN EXITOSA!")
        
        # Verificar tablas
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        # Contar productos existentes
        cursor.execute("SELECT COUNT(*) FROM productos")
        count = cursor.fetchone()[0]
        print(f"📊 Productos en la tabla: {count}")
        
        # Probar inserción de prueba
        print("Probando inserción...")
        result = Producto.crear_producto("Producto de Prueba SQLite", 99.99, 10)
        if result:
            print(f"✅ INSERCIÓN EXITOSA! ID del producto: {result}")
            
            # Eliminar el producto de prueba
            if Producto.eliminar_producto(result):
                print("🗑️ Producto de prueba eliminado")
            
        connection.close()
        print("✅ TODAS LAS PRUEBAS EXITOSAS!")
    else:
        print("❌ No se pudo obtener conexión")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    
print("\n=== FIN DE LA PRUEBA ===")