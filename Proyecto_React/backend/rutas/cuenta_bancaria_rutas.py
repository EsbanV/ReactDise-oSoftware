from flask import Blueprint, request, jsonify, session, current_app

cuenta_rutas = Blueprint('cuenta_rutas', __name__)

@cuenta_rutas.route('/', methods=['GET'])
def obtener_cuentas():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para ver tus cuentas.'}), 401
    cuentas = current_app.cuenta_bancaria_facade.obtener_cuentas(usuario_id)
    cuentas_json = [
        {'id': c.id, 'nombre': c.nombre, 'saldo': c.saldo}
        for c in cuentas
    ]
    return jsonify({'success': True, 'cuentas': cuentas_json})

@cuenta_rutas.route('/', methods=['POST'])
def crear_cuenta():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para crear una cuenta.'}), 401
    data = request.get_json()
    nombre = data.get('nombre')
    saldo_inicial = data.get('saldo_inicial', 0)
    try:
        saldo_inicial = float(saldo_inicial)
    except (TypeError, ValueError):
        saldo_inicial = 0
    try:
        cuenta = current_app.cuenta_bancaria_facade.crear_cuenta(nombre, saldo_inicial, usuario_id)
        return jsonify({'success': True, 'cuenta': {
            'id': cuenta.id, 'nombre': cuenta.nombre, 'saldo': cuenta.saldo
        }}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@cuenta_rutas.route('/<int:cuenta_id>', methods=['GET'])
def obtener_cuenta(cuenta_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        return jsonify({'success': False, 'error': 'Cuenta no encontrada.'}), 404
    return jsonify({'success': True, 'cuenta': {
        'id': cuenta.id, 'nombre': cuenta.nombre, 'saldo': cuenta.saldo
    }})

@cuenta_rutas.route('/<int:cuenta_id>', methods=['PUT'])
def actualizar_cuenta(cuenta_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        return jsonify({'success': False, 'error': 'Cuenta no encontrada.'}), 404
    data = request.get_json()
    nombre = data.get('nombre', cuenta.nombre)
    saldo = data.get('saldo', cuenta.saldo)
    try:
        saldo = float(saldo)
    except (TypeError, ValueError):
        saldo = cuenta.saldo
    try:
        current_app.cuenta_bancaria_facade.actualizar_cuenta(cuenta_id, nombre, saldo)
        return jsonify({'success': True, 'message': 'Cuenta actualizada exitosamente.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@cuenta_rutas.route('/<int:cuenta_id>', methods=['DELETE'])
def eliminar_cuenta(cuenta_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    try:
        current_app.cuenta_bancaria_facade.eliminar_cuenta(cuenta_id)
        return jsonify({'success': True, 'message': 'Cuenta eliminada.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@cuenta_rutas.route('/<int:cuenta_id>/categorias', methods=['GET'])
def categorias_por_cuenta(cuenta_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    categorias = current_app.categoria_facade.obtener_categorias(cuenta_id)
    lista = [
        {"id": c.id, "nombre": c.nombre, "tipo": c.tipo}
        for c in categorias
    ]
    return jsonify({'success': True, 'categorias': lista})
