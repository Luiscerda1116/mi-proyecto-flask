from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from database import execute_query

class User(UserMixin):
    def __init__(self, id_usuario, nombre, email, password=None):
        self.id = str(id_usuario)
        self.nombre = nombre
        self.email = email
        self.password = password

    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_id(user_id):
        """Obtener usuario por ID"""
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        result = execute_query(query, (user_id,))
        
        if result and len(result) > 0:
            user_data = result[0]
            return User(
                user_data['id_usuario'],
                user_data['nombre'],
                user_data['email'],
                user_data['password']
            )
        return None

    @staticmethod
    def get_by_email(email):
        """Obtener usuario por email"""
        query = "SELECT * FROM usuarios WHERE email = %s"
        result = execute_query(query, (email,))
        
        if result and len(result) > 0:
            user_data = result[0]
            return User(
                user_data['id_usuario'],
                user_data['nombre'],
                user_data['email'],
                user_data['password']
            )
        return None

    @staticmethod
    def create_user(nombre, email, password):
        """Crear un nuevo usuario"""
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        result = execute_query(query, (nombre, email, hashed_password))
        return result is not None and result > 0