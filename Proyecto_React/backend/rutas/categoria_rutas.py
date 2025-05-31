from flask import Blueprint, request, jsonify, session, current_app

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/', methods=['POST'])
def crear_categoria():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401

    data = request.get_json()
    try:
        cuenta_id = int(data.get('cuenta_id'))
        if not cuenta_id:
            return jsonify({'success': False, 'error': 'Debes seleccionar una cuenta para crear la categoría.'}), 400

        nombre = data.get('nombre')
        tipo = data.get('tipo')
        presupuesto_valor = data.get('presupuesto', '')

        # Si es string, hacer strip, si es número, convertir directamente
        if isinstance(presupuesto_valor, str):
            presupuesto_valor = presupuesto_valor.strip()

        if presupuesto_valor == '':
            presupuesto = None
        else:
            presupuesto = float(presupuesto_valor)

        categoria = current_app.categoria_facade.crear_categoria(nombre, tipo, presupuesto, cuenta_id)
        return jsonify({'success': True, 'id': categoria.id, 'nombre': categoria.nombre}), 201
    except (TypeError, ValueError) as e:
        return jsonify({'success': False, 'error': f'Error al crear la categoría: {e}'}), 400

@categoria_rutas.route('/', methods=['GET'])
def listar_categorias():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401

    cuenta_id = request.args.get('cuenta_id', type=int)
    tipo = request.args.get('tipo')
    categorias = current_app.categoria_facade.obtener_categorias_filtradas(cuenta_id, tipo)

    data = [
        {
            "id": c.id,
            "nombre": c.nombre,
            "tipo": c.tipo.value if hasattr(c.tipo, 'value') else c.tipo,
            "presupuesto": c.presupuesto.monto_asignado if c.presupuesto else None
        }
        for c in categorias
    ]
    return jsonify({'success': True, 'categorias': data})

@categoria_rutas.route('/<int:categoria_id>', methods=['PUT'])
def actualizar_categoria(categoria_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401

    categoria = current_app.categoria_facade.obtener_categoria_por_id(categoria_id)
    if not categoria:
        return jsonify({'success': False, 'error': 'Categoría no encontrada.'}), 404

    data = request.get_json()
    nuevo_nombre = data.get('nombre', categoria.nombre)
    try:
        current_app.categoria_facade.actualizar_categoria(categoria_id, nuevo_nombre)
        return jsonify({'success': True, 'message': 'Categoría actualizada.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@categoria_rutas.route('/<int:categoria_id>', methods=['DELETE'])
def eliminar_categoria(categoria_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401

    categoria = current_app.categoria_facade.obtener_categoria_por_id(categoria_id)
    if not categoria:
        return jsonify({'success': False, 'error': 'Categoría no encontrada.'}), 404

    try:
        current_app.categoria_facade.eliminar_categoria(categoria_id)
        return jsonify({'success': True, 'message': 'Categoría eliminada.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
