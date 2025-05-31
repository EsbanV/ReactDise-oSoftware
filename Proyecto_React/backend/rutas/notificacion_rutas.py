from flask import Blueprint, jsonify, session, current_app, request

notificacion_rutas = Blueprint('notificacion_rutas', __name__, url_prefix='/api/notificaciones')

@notificacion_rutas.route('/<int:notificacion_id>', methods=['PATCH'])
def marcar_leida(notificacion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    # Podrías aceptar en el body si quieres marcar como leída/no leída, ej: {"leida": true}
    data = request.get_json(silent=True) or {}
    leida = data.get('leida', True)  # Por defecto True si no se especifica

    try:
        current_app.comunidad_facade.marcar_notificacion_leida(notificacion_id, leida)
        return jsonify({'success': True, 'message': f'Notificación marcada como {"leída" if leida else "no leída"}.', 'notificacion_id': notificacion_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400