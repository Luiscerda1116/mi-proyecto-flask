from database import execute_query

# Test: crear un usuario
print("🧪 Probando crear usuario...")
resultado = execute_query(
    "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
    ('Test User', 'test@example.com', 'password_hash_123')
)

if resultado and resultado > 0:
    print("✅ Usuario creado exitosamente")
    
    # Test: buscar el usuario
    print("🔍 Buscando usuario...")
    usuarios = execute_query("SELECT * FROM usuarios WHERE email = %s", ('test@example.com',))
    
    if usuarios:
        print(f"✅ Usuario encontrado: {usuarios[0]['nombre']}")
    else:
        print("❌ No se encontró el usuario")
else:
    print("❌ Error al crear usuario")