import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Crear conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='desarrollo_web',
            port=3306,
            autocommit=True
        )
        return connection
    except Error as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        return None

def execute_query(query, params=None):
    """Ejecutar una consulta y devolver los resultados"""
    connection = get_db_connection()
    if connection is None:
        print("❌ No se pudo establecer conexión a la base de datos")
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
        
        cursor.close()
        connection.close()
        return result
        
    except Error as e:
        print(f"❌ Error ejecutando consulta: {e}")
        if connection:
            connection.close()
        return None