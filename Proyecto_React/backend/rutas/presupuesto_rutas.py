from flask import Blueprint, request, jsonify, session, current_app

presupuesto_rutas = Blueprint('presupuesto_rutas', __name__)

@presupuesto_rutas.route('/', methods=['GET'])
def obtener_presupuestos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401

    categorias = current_app.categoria_facade.obtener_categorias_por_usuario(usuario_id)
    presupuestos = {}
    for categoria in categorias:
        presupuesto = current_app.presupuesto_facade.obtener_presupuesto(categoria.id)
        presupuestos[categoria.id] = presupuesto

    categorias_json = [
        {
            'id': categoria.id,
            'nombre': categoria.nombre,
            'tipo': categoria.tipo.value if hasattr(categoria.tipo, 'value') else categoria.tipo,
            'presupuesto': presupuestos.get(categoria.id)
        }
        for categoria in categorias
    ]
    return jsonify({'success': True, 'categorias': categorias_json})

@presupuesto_rutas.route('/', methods=['POST'])
def asignar_presupuestos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401

    categorias = current_app.categoria_facade.obtener_categorias_por_usuario(usuario_id)
    data = request.get_json()
    presupuestos_actualizados = []
    errores = []

    for categoria in categorias:
        monto = data.get(str(categoria.id)) or data.get(categoria.id)
        if monto is not None:
            try:
                monto = float(monto)
                current_app.presupuesto_facade.asignar_presupuesto(categoria.id, monto)
                presupuestos_actualizados.append({'categoria_id': categoria.id, 'monto': monto})
            except ValueError:
                errores.append({'categoria_id': categoria.id, 'error': 'Monto inválido'})

    if errores:
        return jsonify({'success': False, 'error': 'Algunos montos inválidos', 'errores': errores}), 400
    return jsonify({'success': True, 'message': 'Presupuestos actualizados correctamente.', 'actualizados': presupuestos_actualizados})

@presupuesto_rutas.route('/<int:presupuesto_id>/', methods=['DELETE'])
def eliminar_presupuesto(presupuesto_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401
    try:
        current_app.presupuesto_facade.eliminar_presupuesto(presupuesto_id)
        return jsonify({'success': True, 'message': 'Presupuesto eliminado.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
