from flask import Blueprint, request, session, jsonify, current_app

usuario_rutas = Blueprint('usuario_rutas', __name__)

@usuario_rutas.route('/', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    if not nombre or not correo or not contrasena:
        return jsonify({'success': False, 'error': 'Todos los campos son requeridos.'}), 400
    try:
        usuario = current_app.usuario_facade.registrar_usuario(nombre, correo, contrasena)
        return jsonify({'success': True, 'usuario': {'id': usuario.id, 'nombre': usuario.nombre}})
    except Exception as e:
        current_app.logger.error("Error al registrar usuario: %s", e)
        return jsonify({'success': False, 'error': str(e)}), 400

@usuario_rutas.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    try:
        usuario = current_app.usuario_facade.iniciar_sesion(correo, contrasena)
        if usuario:
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            session['logged_in'] = True
            return jsonify({'success': True, 'usuario': {'id': usuario.id, 'nombre': usuario.nombre}})
        else:
            return jsonify({'success': False, 'error': 'Credenciales inválidas.'}), 401
    except Exception as e:
        current_app.logger.error("Error al iniciar sesión: %s", e)
        return jsonify({'success': False, 'error': str(e)}), 401

@usuario_rutas.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario_id', None)
    session.pop('nombre', None)
    session.pop('logged_in', None)
    return jsonify({'success': True, 'message': 'Sesión cerrada.'})

@usuario_rutas.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    try:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
        return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'correo': usuario.correo})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@usuario_rutas.route('/session', methods=['GET'])
def verificar_sesion():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
        return jsonify({'loggedIn': True, 'usuario': {'id': usuario.id, 'nombre': usuario.nombre}})
    return jsonify({'loggedIn': False}), 401
