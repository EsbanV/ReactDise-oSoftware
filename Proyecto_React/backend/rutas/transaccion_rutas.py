from flask import Blueprint, request, jsonify, session, current_app

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/', methods=['POST'])
def registrar_transaccion():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para registrar transacciones.'}), 401

    data = request.get_json()
    cuenta_id = data.get('cuenta_id')
    categoria_id = data.get('categoria_id')
    descripcion = data.get('descripcion', '')
    monto = data.get('monto')

    if not (cuenta_id and categoria_id and monto):
        return jsonify({'success': False, 'error': 'Faltan campos obligatorios.'}), 400

    try:
        current_app.transaccion_facade.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto, fecha=None)
        # Si quieres retornar el nuevo saldo actualizado, puedes hacerlo así:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        return jsonify({
            'success': True,
            'message': 'Transacción registrada correctamente.',
            'nuevo_saldo': cuenta.saldo if cuenta else None
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al registrar la transacción: {str(e)}'}), 400

@transaccion_rutas.route('/', methods=['GET'])
def listar_transacciones():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401

    cuenta_id = request.args.get('cuenta_id', type=int)
    if not cuenta_id:
        return jsonify({'success': False, 'error': 'Falta el ID de la cuenta.'}), 400

    transacciones = current_app.transaccion_facade.obtener_transacciones_por_cuenta(cuenta_id)
    data = [
        {
            'id': t.id,
            'cuenta_id': t.cuenta_bancaria_id,
            'categoria_id': t.categoria_id,
            'descripcion': t.descripcion,
            'monto': t.monto,
            'fecha': str(t.fecha)
        }
        for t in transacciones
    ]
    return jsonify({'success': True, 'transacciones': data})
