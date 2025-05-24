from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, jsonify, current_app
from models import db, Usuario
from datetime import datetime, time, timedelta
from flask_login import login_user, login_required, current_user, logout_user
from functools import wraps
import pytz
import re


main_routes = Blueprint('main', __name__)

# Decorador para verificar si el usuario es admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.rol != 'admin':
            flash('No tienes permiso para acceder a esta página', 'danger')
            return redirect(url_for('main.login'))  # Redirigir al login si no es admin
        return f(*args, **kwargs)
    return decorated_function



@main_routes.route('/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            nombreuser = request.form.get('nombreuser', '').strip()
            password = request.form.get('password', '').strip()
            
            # Validaciones básicas
            if not nombreuser or not password:
                flash('Todos los campos son obligatorios', 'danger')
                return redirect(url_for('main.login'))
            
            # Buscar al usuario por nombre de usuario
            usuario = db.session.query(Usuario).filter_by(nombreuser=nombreuser).first()
            
            if not usuario:
                flash('Este usuario no es válido', 'danger')  # Mensaje genérico por seguridad
                return redirect(url_for('main.login'))
            
            # Verificar si es admin
            if usuario.rol != 'admin':
                flash('Acceso restringido a solo administradores', 'danger')
                return redirect(url_for('main.login'))
            
            # Verificar contraseña
            if usuario.check_password(password):
                login_user(usuario)
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('main.clientes'))
            else:
                flash('Contraseña inválida', 'danger')
                
    except Exception as e:
        current_app.logger.error(f'Error en login: {str(e)}')
        flash('Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde.', 'danger')
    
    return render_template('login.html')



@main_routes.route('/clientes', methods=['GET', 'POST'])
def clientes():
    return render_template('clientes.html')

@main_routes.route('/logout')
@admin_required
def logout():
    logout_user()  # Cierra la sesión
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('main.login'))

@main_routes.route('/usuarios')
@admin_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@main_routes.route('/toggle_block/<int:user_id>', methods=['POST'])
@admin_required
def toggle_block(user_id):
    try:
        usuario = Usuario.query.filter_by(usuario_id=user_id).first_or_404()
        # No permitir que un admin se desactive a sí mismo
        if usuario.usuario_id == current_user.usuario_id:
            return jsonify({'success': False, 'message': 'No puedes desactivarte a ti mismo'}), 400
        
        usuario.status = not usuario.status
        db.session.commit()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        current_app.logger.error(f'Error al cambiar estado del usuario: {str(e)}')
        return jsonify({'success': False, 'message': 'Error al procesar la solicitud'}), 500
