from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Numeric, Enum
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20))  # Aumenté el tamaño para acomodar el + y espacios
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin'), nullable=False)
    isBlocked = db.Column(db.Boolean, default=False)
    perfil = db.Column(db.String(255))

    def __repr__(self):
        return f"<Usuario {self.nombre} - {self.email}>"

    def set_password(self, password):
        """Generar y asignar el hash de la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verificar si la contraseña proporcionada coincide con el hash almacenado"""
        return check_password_hash(self.password, password)

