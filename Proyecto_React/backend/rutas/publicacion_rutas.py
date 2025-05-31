from flask import Blueprint, request, jsonify, session, abort, current_app

publicacion_rutas = Blueprint('publicacion_rutas', __name__, url_prefix='/api/publicaciones')

# Crear una publicación
@publicacion_rutas.route('/', methods=['POST'])
def crear_publicacion():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    data = request.get_json()
    titulo    = data.get('titulo', '').strip()
    contenido = data.get('contenido', '').strip()
    if not (titulo and contenido):
        return jsonify({'success': False, 'error': 'Faltan datos requeridos.', 'titulo': titulo, 'contenido': contenido}), 400
    try:
        publicacion = current_app.comunidad_facade.crear_publicacion(usuario_id, titulo, contenido)
        return jsonify({'success': True, 'message': 'Publicación creada.', 'publicacion_id': publicacion.id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al crear la publicación: {e}'}), 400

# Listar todas las publicaciones
@publicacion_rutas.route('/', methods=['GET'])
def listar_publicaciones():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        publicaciones = current_app.comunidad_facade.obtener_publicaciones()
        resultado = [publicacion.to_dict() for publicacion in publicaciones]
        return jsonify({'success': True, 'publicaciones': resultado}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al obtener publicaciones: {e}'}), 500

# Ver una publicación y sus comentarios
@publicacion_rutas.route('/<int:publicacion_id>', methods=['GET'])
def obtener_publicacion(publicacion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401
    try:
        publicacion = current_app.comunidad_facade.obtener_publicacion(publicacion_id)
        return jsonify({'success': True, 'publicacion': publicacion.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al obtener la publicación: {e}'}), 404

# Crear un comentario en una publicación
@publicacion_rutas.route('/<int:publicacion_id>/comentarios', methods=['POST'])
def crear_comentario(publicacion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    data = request.get_json()
    contenido = data.get('contenido', '').strip()
    if not contenido:
        return jsonify({'success': False, 'error': 'Falta el contenido del comentario.'}), 400
    try:
        comentario = current_app.comunidad_facade.agregar_comentario(publicacion_id, usuario_id, contenido)
        return jsonify({'success': True, 'message': 'Comentario agregado.', 'comentario': comentario.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al agregar comentario: {e}'}), 400
