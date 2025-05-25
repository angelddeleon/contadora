from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint, jsonify, current_app
from models import db, Usuario, LibroCompra, LibroVenta, Cliente
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
@admin_required
def clientes():
    try:
        clientes = Cliente.query.all()
        return render_template('clientes.html', clientes=clientes)
    except Exception as e:
        current_app.logger.error(f'Error al cargar clientes: {str(e)}')
        flash('Error al cargar la lista de clientes', 'danger')
        return redirect(url_for('main.login'))

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

@main_routes.route('/librocompra')
@admin_required
def librocompra():
    try:
        compras = LibroCompra.query.all()
        return render_template('librocompra.html', compras=compras)
    except Exception as e:
        current_app.logger.error(f'Error al cargar libro de compras: {str(e)}')
        flash('Error al cargar el libro de compras', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/libroventa')
@admin_required
def libroventa():
    try:
        ventas = LibroVenta.query.all()
        return render_template('libroventa.html', ventas=ventas)
    except Exception as e:
        current_app.logger.error(f'Error al cargar libro de ventas: {str(e)}')
        flash('Error al cargar el libro de ventas', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/editar_compra/<int:compra_id>', methods=['GET', 'POST'])
@admin_required
def editar_compra(compra_id):
    compra = LibroCompra.query.get_or_404(compra_id)
    if request.method == 'POST':
        try:
            # Aquí irá la lógica para actualizar la compra
            flash('Compra actualizada con éxito', 'success')
            return redirect(url_for('main.librocompra'))
        except Exception as e:
            current_app.logger.error(f'Error al editar compra: {str(e)}')
            flash('Error al editar la compra', 'danger')
    return render_template('editar_compra.html', compra=compra)

@main_routes.route('/editar_venta/<int:venta_id>', methods=['GET', 'POST'])
@admin_required
def editar_venta(venta_id):
    venta = LibroVenta.query.get_or_404(venta_id)
    if request.method == 'POST':
        try:
            # Aquí irá la lógica para actualizar la venta
            flash('Venta actualizada con éxito', 'success')
            return redirect(url_for('main.libroventa'))
        except Exception as e:
            current_app.logger.error(f'Error al editar venta: {str(e)}')
            flash('Error al editar la venta', 'danger')
    return render_template('editar_venta.html', venta=venta)

@main_routes.route('/eliminar_compra/<int:compra_id>', methods=['POST'])
@admin_required
def eliminar_compra(compra_id):
    try:
        compra = LibroCompra.query.get_or_404(compra_id)
        db.session.delete(compra)
        db.session.commit()
        flash('Compra eliminada con éxito', 'success')
    except Exception as e:
        current_app.logger.error(f'Error al eliminar compra: {str(e)}')
        flash('Error al eliminar la compra', 'danger')
    return redirect(url_for('main.librocompra'))

@main_routes.route('/eliminar_venta/<int:venta_id>', methods=['POST'])
@admin_required
def eliminar_venta(venta_id):
    try:
        venta = LibroVenta.query.get_or_404(venta_id)
        db.session.delete(venta)
        db.session.commit()
        flash('Venta eliminada con éxito', 'success')
    except Exception as e:
        current_app.logger.error(f'Error al eliminar venta: {str(e)}')
        flash('Error al eliminar la venta', 'danger')
    return redirect(url_for('main.libroventa'))

@main_routes.route('/toggle_status/<int:cliente_id>', methods=['POST'])
@admin_required
def toggle_status(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        # Cambiar el estado entre 'activo' e 'inactivo'
        cliente.status = 'inactivo' if cliente.status == 'activo' else 'activo'
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        current_app.logger.error(f'Error al cambiar estado del cliente: {str(e)}')
        return jsonify({'success': False, 'message': 'Error al procesar la solicitud'}), 500

@main_routes.route('/cliente/<int:cliente_id>/libro-ventas')
@admin_required
def cliente_libro_ventas(cliente_id):
    try:
        print(f"Accediendo a libro de ventas para cliente ID: {cliente_id}")  # Debug
        cliente = Cliente.query.get_or_404(cliente_id)
        print(f"Cliente encontrado: {cliente.nombre}")  # Debug
        ventas = LibroVenta.query.filter_by(id_cliente=cliente_id).all()
        print(f"Número de ventas encontradas: {len(ventas)}")  # Debug
        return render_template('libroventa.html', ventas=ventas, cliente=cliente, filtro_cliente=True)
    except Exception as e:
        current_app.logger.error(f'Error al cargar libro de ventas del cliente: {str(e)}')
        print(f"Error en libro de ventas: {str(e)}")  # Debug
        flash('Error al cargar el libro de ventas del cliente', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/cliente/<int:cliente_id>/libro-compras')
@admin_required
def cliente_libro_compras(cliente_id):
    try:
        print(f"Accediendo a libro de compras para cliente ID: {cliente_id}")  # Debug
        cliente = Cliente.query.get_or_404(cliente_id)
        print(f"Cliente encontrado: {cliente.nombre}")  # Debug
        compras = LibroCompra.query.filter_by(id_cliente=cliente_id).all()
        print(f"Número de compras encontradas: {len(compras)}")  # Debug
        return render_template('librocompra.html', compras=compras, cliente=cliente, filtro_cliente=True)
    except Exception as e:
        current_app.logger.error(f'Error al cargar libro de compras del cliente: {str(e)}')
        print(f"Error en libro de compras: {str(e)}")  # Debug
        flash('Error al cargar el libro de compras del cliente', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/cliente/<int:cliente_id>')
@admin_required
def ver_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return render_template('ver_cliente.html', cliente=cliente)
    except Exception as e:
        current_app.logger.error(f'Error al cargar detalles del cliente: {str(e)}')
        flash('Error al cargar los detalles del cliente', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/crear_cliente', methods=['GET'])
@admin_required
def mostrar_crear_cliente():
    try:
        return render_template('crear_cliente.html')
    except Exception as e:
        current_app.logger.error(f'Error al mostrar formulario de cliente: {str(e)}')
        flash('Error al cargar el formulario', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/crear_cliente', methods=['POST'])
@admin_required
def crear_cliente():
    try:
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        representante = request.form.get('representante')
        rif = request.form.get('rif')
        nit = request.form.get('nit')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        numero = request.form.get('numero')
        contribuyente = request.form.get('contribuyente')  # Ahora será 'ordinario' o 'especial'
        registradora = request.form.get('registradora')
        clasificacion = request.form.get('clasificacion')
        usuarioseniat = request.form.get('usuarioseniat')
        claveseniat = request.form.get('claveseniat')
        clavepatente = request.form.get('clavepatente')
        directoriocomo = request.form.get('directoriocomo')
        
        # Validar campos requeridos
        if not nombre:
            flash('El nombre del cliente es requerido', 'danger')
            return redirect(url_for('main.mostrar_crear_cliente'))
            
        if contribuyente not in ['ordinario', 'especial']:
            flash('El tipo de contribuyente debe ser ordinario o especial', 'danger')
            return redirect(url_for('main.mostrar_crear_cliente'))
            
        # Crear nuevo cliente
        nuevo_cliente = Cliente(
            nombre=nombre,
            representante=representante,
            rif=rif,
            nit=nit,
            direccion=direccion,
            telefono=telefono,
            numero=numero,
            contribuyente=contribuyente,
            registradora=registradora,
            clasificacion=clasificacion,
            usuarioseniat=usuarioseniat,
            claveseniat=claveseniat,
            clavepatente=clavepatente,
            directoriocomo=directoriocomo,
            status='activo'
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('main.clientes'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al crear cliente: {str(e)}')
        flash('Error al crear el cliente', 'danger')
        return redirect(url_for('main.mostrar_crear_cliente'))

@main_routes.route('/crear-venta', methods=['GET', 'POST'])
@admin_required
def crear_venta():
    cliente_id = request.args.get('cliente_id')
    current_app.logger.debug(f"Iniciando crear_venta con cliente_id: {cliente_id}")
    
    if not cliente_id:
        flash('Se requiere especificar un cliente', 'danger')
        return redirect(url_for('main.clientes'))
        
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        current_app.logger.debug(f"Cliente encontrado: {cliente.nombre}")
        
        if request.method == 'POST':
            current_app.logger.debug("Procesando POST request")
            current_app.logger.debug(f"Datos del formulario: {request.form}")
            
            try:
                nueva_venta = LibroVenta(
                    id_cliente=int(cliente_id),
                    numerofactura=request.form['numerofactura'],
                    fechafactura=datetime.strptime(request.form['fechafactura'], '%Y-%m-%d'),
                    rif=request.form['rif'],
                    cliente=request.form['nombre_cliente'],
                    montoTotal=float(request.form['montoTotal']),
                    base=float(request.form['base']),
                    iva=float(request.form['iva']),
                    exentas=float(request.form['exentas']) if request.form.get('exentas') else 0.00,
                    documento=request.form.get('documento', 'Factura')
                )
                
                current_app.logger.debug("Nueva venta creada, intentando guardar en la base de datos")
                db.session.add(nueva_venta)
                db.session.commit()
                
                current_app.logger.debug("Venta guardada exitosamente")
                flash('Venta creada exitosamente', 'success')
                return redirect(url_for('main.cliente_libro_ventas', cliente_id=cliente_id))
                
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error al crear la venta: {str(e)}')
                current_app.logger.exception("Excepción completa:")
                flash(f'Error al crear la venta: {str(e)}', 'danger')
                return render_template('crear_venta.html', cliente=cliente)
        
        # GET request
        return render_template('crear_venta.html', cliente=cliente)
        
    except Exception as e:
        current_app.logger.error(f'Error al acceder al cliente: {str(e)}')
        current_app.logger.exception("Excepción completa:")
        flash('Error al acceder al cliente', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/crear-compra', methods=['GET', 'POST'])
@admin_required
def crear_compra():
    cliente_id = request.args.get('cliente_id')
    if not cliente_id:
        flash('Se requiere especificar un cliente', 'danger')
        return redirect(url_for('main.clientes'))
        
    cliente = Cliente.query.get_or_404(cliente_id)
    
    if request.method == 'POST':
        try:
            nueva_compra = LibroCompra(
                id_cliente=cliente_id,
                numerofactura=request.form['numerofactura'],
                control=request.form['control'],
                fechafactura=datetime.strptime(request.form['fechafactura'], '%Y-%m-%d'),
                rif=request.form['rif_proveedor'],
                provedor=request.form['provedor'],
                montoTotal=float(request.form['montoTotal']),
                base=float(request.form['base']),
                iva=float(request.form['iva']),
                exentas=float(request.form['exentas']) if request.form['exentas'] else 0.00,
                facturapolar=True if request.form.get('facturapolar') else False,
                documento=request.form.get('documento', 'Factura')
            )
            
            db.session.add(nueva_compra)
            db.session.commit()
            
            flash('Compra creada exitosamente', 'success')
            return redirect(url_for('main.cliente_libro_compras', cliente_id=cliente_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la compra: {str(e)}', 'error')
            return redirect(url_for('main.crear_compra', cliente_id=cliente_id))
    
    # GET request
    return render_template('crear_compra.html', cliente=cliente)

@main_routes.route('/editar_cliente/<int:cliente_id>', methods=['GET'])
@admin_required
def mostrar_editar_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return render_template('editar_cliente.html', cliente=cliente)
    except Exception as e:
        current_app.logger.error(f'Error al cargar formulario de edición: {str(e)}')
        flash('Error al cargar el formulario de edición', 'danger')
        return redirect(url_for('main.clientes'))

@main_routes.route('/editar_cliente/<int:cliente_id>', methods=['POST'])
@admin_required
def editar_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Actualizar datos del cliente
        cliente.nombre = request.form.get('nombre')
        cliente.representante = request.form.get('representante')
        cliente.rif = request.form.get('rif')
        cliente.nit = request.form.get('nit')
        cliente.direccion = request.form.get('direccion')
        cliente.telefono = request.form.get('telefono')
        cliente.numero = request.form.get('numero')
        cliente.contribuyente = request.form.get('contribuyente')
        cliente.registradora = request.form.get('registradora')
        cliente.clasificacion = request.form.get('clasificacion')
        cliente.usuarioseniat = request.form.get('usuarioseniat')
        
        # Solo actualizar la clave SENIAT si se proporciona una nueva
        nueva_clave_seniat = request.form.get('claveseniat')
        if nueva_clave_seniat:
            cliente.claveseniat = nueva_clave_seniat
            
        cliente.clavepatente = request.form.get('clavepatente')
        cliente.directoriocomo = request.form.get('directoriocomo')
        
        db.session.commit()
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('main.ver_cliente', cliente_id=cliente_id))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al actualizar cliente: {str(e)}')
        flash('Error al actualizar el cliente', 'danger')
        return redirect(url_for('main.mostrar_editar_cliente', cliente_id=cliente_id))
