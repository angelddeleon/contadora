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
    

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    representante = db.Column(db.String(100))
    rif = db.Column(db.String(20), unique=True)
    nit = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    numero = db.Column(db.String(20))
    contribuyente = db.Column(db.Boolean, default=False)
    registradora = db.Column(db.String(50))
    clasificacion = db.Column(db.String(50))
    usuarioseniat = db.Column(db.String(50))
    claveseniat = db.Column(db.String(100))
    status = db.Column(db.Enum('activo', 'inactivo', name='statusenum'), default='activo')
    clavepatente = db.Column(db.String(50))
    directoriocomo = db.Column(db.String(255))
    
    def __init__(self, nombre, representante=None, rif=None, nit=None, 
                 direccion=None, telefono=None, numero=None, contribuyente=False,
                 registradora=None, clasificacion=None, usuarioseniat=None,
                 claveseniat=None, status='activo', clavepatente=None,
                 directoriocomo=None):
        self.nombre = nombre
        self.representante = representante
        self.rif = rif
        self.nit = nit
        self.direccion = direccion
        self.telefono = telefono
        self.numero = numero
        self.contribuyente = contribuyente
        self.registradora = registradora
        self.clasificacion = clasificacion
        self.usuarioseniat = usuarioseniat
        self.claveseniat = claveseniat
        self.status = status
        self.clavepatente = clavepatente
        self.directoriocomo = directoriocomo
    
    def __repr__(self):
        return f'<Cliente {self.id_cliente}: {self.nombre} - {self.rif}>'
    
    def to_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nombre': self.nombre,
            'representante': self.representante,
            'rif': self.rif,
            'nit': self.nit,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'numero': self.numero,
            'contribuyente': self.contribuyente,
            'registradora': self.registradora,
            'clasificacion': self.clasificacion,
            'usuarioseniat': self.usuarioseniat,
            'claveseniat': self.claveseniat,
            'status': self.status,  # Ya no necesitamos .value porque es un string
            'clavepatente': self.clavepatente,
            'directoriocomo': self.directoriocomo
        }