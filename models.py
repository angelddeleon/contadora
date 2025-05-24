from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Numeric, Enum
from datetime import datetime
from decimal import Decimal

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
    contribuyente = db.Column(db.Enum('ordinario', 'especial', name='tipo_contribuyente'), nullable=False, default='ordinario')
    registradora = db.Column(db.String(50))
    clasificacion = db.Column(db.String(50))
    usuarioseniat = db.Column(db.String(50))
    claveseniat = db.Column(db.String(100))
    status = db.Column(db.Enum('activo', 'inactivo', name='statusenum'), default='activo')
    clavepatente = db.Column(db.String(50))
    directoriocomo = db.Column(db.String(255))
    
    def __init__(self, nombre, representante=None, rif=None, nit=None, 
                 direccion=None, telefono=None, numero=None, contribuyente='ordinario',
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


class LibroVenta(db.Model):
    __tablename__ = 'libro_ventas'
    
    idfacturaventa = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    numerofactura = db.Column(db.String(50), unique=True, nullable=False)
    fechar = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Fecha de registro
    fechafactura = db.Column(db.Date, nullable=False)  # Fecha de la factura
    rif = db.Column(db.String(20), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)  # Nombre del cliente
    montoTotal = db.Column(db.Numeric(12, 2), nullable=False)
    exentas = db.Column(db.Numeric(12, 2), default=0.00)
    base = db.Column(db.Numeric(12, 2), nullable=False)  # Base imponible
    cajaregistradora = db.Column(db.String(50))
    porcentaje_iva = db.Column(db.Numeric(5, 2), default=16.00)  # % de IVA
    iva = db.Column(db.Numeric(12, 2), nullable=False)  # Monto de IVA
    
    # Relación con Cliente
    cliente_rel = db.relationship('Cliente', backref='ventas')
    
    def __init__(self, id_cliente, numerofactura, fechafactura, rif, cliente, 
                 montoTotal, base, iva, exentas=0.00, cajaregistradora=None, 
                 porcentaje_iva=16.00):
        self.id_cliente = id_cliente
        self.numerofactura = numerofactura
        self.fechar = datetime.utcnow().date()
        self.fechafactura = fechafactura
        self.rif = rif
        self.cliente = cliente
        self.montoTotal = montoTotal
        self.exentas = exentas
        self.base = base
        self.cajaregistradora = cajaregistradora
        self.porcentaje_iva = porcentaje_iva
        self.iva = iva
    
    def __repr__(self):
        return f'<LibroVenta {self.numerofactura} - {self.cliente}>'
    
    def to_dict(self):
        return {
            'idfacturaventa': self.idfacturaventa,
            'id_cliente': self.id_cliente,
            'numerofactura': self.numerofactura,
            'fechar': self.fechar.isoformat(),
            'fechafactura': self.fechafactura.isoformat(),
            'rif': self.rif,
            'cliente': self.cliente,
            'montoTotal': float(self.montoTotal),
            'exentas': float(self.exentas),
            'base': float(self.base),
            'cajaregistradora': self.cajaregistradora,
            'porcentaje_iva': float(self.porcentaje_iva),
            'iva': float(self.iva),
            'cliente_info': {
                'nombre': self.cliente_rel.nombre if self.cliente_rel else None,
                'telefono': self.cliente_rel.telefono if self.cliente_rel else None
            }
        }



class LibroCompra(db.Model):
    __tablename__ = 'libro_compras'
    
    idfacturacompra = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    numerofactura = db.Column(db.String(50), nullable=False)
    control = db.Column(db.String(50))  # Número de control de la factura
    fechar = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Fecha de registro
    fechafactura = db.Column(db.Date, nullable=False)  # Fecha de la factura
    rif = db.Column(db.String(20), nullable=False)  # RIF del proveedor
    provedor = db.Column(db.String(100), nullable=False)  # Nombre del proveedor
    montoTotal = db.Column(db.Numeric(12, 2), nullable=False)
    exentas = db.Column(db.Numeric(12, 2), default=Decimal('0.00'))
    base = db.Column(db.Numeric(12, 2), nullable=False)  # Base imponible
    facturapolar = db.Column(db.Boolean, default=False)  # Es factura polar?
    documento = db.Column(db.String(20))  # Tipo de documento (Factura, Nota de crédito, etc.)
    porcentaje_iva = db.Column(db.Numeric(5, 2), default=Decimal('16.00'))  # % de IVA
    iva = db.Column(db.Numeric(12, 2), nullable=False)  # Monto de IVA
    
    # Relación con Cliente
    cliente_rel = db.relationship('Cliente', backref='compras')
    
    def __init__(self, id_cliente, numerofactura, fechafactura, rif, provedor, 
                 montoTotal, base, iva, control=None, exentas=0.00, 
                 facturapolar=False, documento=None, porcentaje_iva=16.00):
        self.id_cliente = id_cliente
        self.numerofactura = numerofactura
        self.control = control
        self.fechar = datetime.utcnow().date()
        self.fechafactura = fechafactura
        self.rif = rif
        self.provedor = provedor
        self.montoTotal = montoTotal
        self.exentas = exentas
        self.base = base
        self.facturapolar = facturapolar
        self.documento = documento
        self.porcentaje_iva = porcentaje_iva
        self.iva = iva
    
    def __repr__(self):
        return f'<LibroCompra {self.numerofactura} - {self.provedor}>'
    
    def to_dict(self):
        return {
            'idfacturacompra': self.idfacturacompra,
            'id_cliente': self.id_cliente,
            'numerofactura': self.numerofactura,
            'control': self.control,
            'fechar': self.fechar.isoformat(),
            'fechafactura': self.fechafactura.isoformat(),
            'rif': self.rif,
            'provedor': self.provedor,
            'montoTotal': float(self.montoTotal),
            'exentas': float(self.exentas),
            'base': float(self.base),
            'facturapolar': self.facturapolar,
            'documento': self.documento,
            'porcentaje_iva': float(self.porcentaje_iva),
            'iva': float(self.iva),
            'cliente_info': {
                'nombre': self.cliente_rel.nombre if self.cliente_rel else None,
                'rif': self.cliente_rel.rif if self.cliente_rel else None
            }
        }