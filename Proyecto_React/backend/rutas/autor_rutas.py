from flask import Blueprint, session, request, jsonify, current_app

autor_rutas = Blueprint('autor_rutas', __name__, url_prefix='/api/autores')

@autor_rutas.route('/<int:autor_id>/suscriptores', methods=['POST'])
def suscribir_autor(autor_id):
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        current_app.comunidad_facade.suscribirse_autor(subscriber_id, autor_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

    publicacion_id = request.args.get('from_pub', type=int)
    return jsonify({
        'success': True,
        'message': 'Suscripción realizada correctamente.',
        'autor_id': autor_id,
        'from_publicacion_id': publicacion_id
    })

@autor_rutas.route('/<int:autor_id>/suscriptores', methods=['DELETE'])
def desuscribir_autor(autor_id):
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        current_app.comunidad_facade.desuscribirse_autor(subscriber_id, autor_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

    publicacion_id = request.args.get('from_pub', type=int)
    return jsonify({
        'success': True,
        'message': 'Desuscripción realizada correctamente.',
        'autor_id': autor_id,
        'from_publicacion_id': publicacion_id
    })
