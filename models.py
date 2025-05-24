from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Numeric, Enum
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)  # Cambiado de 'id' a 'usuario_id'
    nombreuser = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario
    nombre = db.Column(db.String(100), nullable=False)  # Nombre
    apellido = db.Column(db.String(100), nullable=False)  # Apellido
    cedula = db.Column(db.String(20), unique=True, nullable=False)  # Cédula
    telefono = db.Column(db.String(20))  # Teléfono
    password = db.Column(db.String(255), nullable=False)  # Contraseña
    rol = db.Column(db.Enum('admin', 'editor', 'ver'), nullable=False)  # Rol con más opciones
    status = db.Column(db.Boolean, default=True)  # Cambiado de 'isBlocked' a 'status' (True=activo, False=inactivo)

    def __repr__(self):
        return f"<Usuario {self.nombreuser} - {self.nombre} {self.apellido}>"

    def set_password(self, password):
        """Generar y asignar el hash de la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verificar si la contraseña proporcionada coincide con el hash almacenado"""
        return check_password_hash(self.password, password)

    def get_id(self):
        """Método requerido por Flask-Login"""
        return str(self.usuario_id)