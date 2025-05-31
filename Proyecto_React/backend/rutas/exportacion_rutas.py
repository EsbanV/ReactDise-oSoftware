from flask import Blueprint, session, request, current_app, send_file, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import tempfile

exportacion_rutas = Blueprint('exportacion_rutas', __name__, url_prefix='/api/exportacion')

@exportacion_rutas.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    usuario_id = session.get('usuario_id')
    cuenta_id = request.args.get('cuenta_id', type=int)
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401
    if not cuenta_id:
        return jsonify({'success': False, 'error': 'Se requiere el ID de la cuenta.'}), 400
    try:
        output, usuario_nombre, nombre_cuenta = current_app.exportacion_facade.exportar_excel(usuario_id, cuenta_id)
        fecha_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'reporte_{usuario_nombre}_{nombre_cuenta}_{fecha_str}.xlsx'

        # Nota: send_file sí puede usarse aquí, pero React debe manejar bien la descarga.
        response = send_file(
            output,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        return response
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500

@exportacion_rutas.route('/importar_excel', methods=['POST'])
def importar_excel():
    archivo = request.files.get('archivo_excel')
    cuenta_id = request.form.get('cuenta_id')
    usuario_id = session.get('usuario_id')

    if not archivo or not cuenta_id or not usuario_id:
        return jsonify({"success": False, "importadas": 0, "errores": ["Faltan datos requeridos."]}), 400

    try:
        cuenta_id = int(cuenta_id)
        usuario_id = int(usuario_id)
    except (ValueError, TypeError):
        return jsonify({"success": False, "importadas": 0, "errores": ["ID de cuenta o usuario inválido."]}), 400

    filename = secure_filename(archivo.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        archivo.save(tmp.name)
        ruta_temporal = tmp.name

    try:
        resultado = current_app.exportacion_facade.importar_excel(ruta_temporal, usuario_id, cuenta_id)
    finally:
        os.remove(ruta_temporal)

    # Siempre responder JSON, sin flash ni redirect
    resultado['success'] = resultado.get('ok', False)
    return jsonify(resultado)
