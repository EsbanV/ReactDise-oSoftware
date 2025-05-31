from flask import Blueprint, jsonify, session, request, current_app

dashboard_rutas = Blueprint('dashboard_rutas', __name__)

@dashboard_rutas.route('/', methods=['GET'])
def dashboard():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    cuenta_id = request.args.get('cuenta_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

    try:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
    except ValueError:
        session.pop('usuario_id', None)
        return jsonify({'success': False, 'error': 'Sesión inválida.'}), 401

    notificaciones = current_app.comunidad_facade.obtener_notificaciones(usuario_id)

    if not cuenta_id:
        cuenta = current_app.cuenta_bancaria_facade.obtener_primer_cuenta(usuario_id)
        cuenta_id = cuenta.id if cuenta else None

    if cuenta_id:
        resumen = current_app.usuario_facade.obtener_resumen(usuario_id, cuenta_id)
        # Gráficos
        if year is not None and month is not None and day is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_dia(cuenta_id, year, month, day)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_dia(cuenta_id, year, month, day)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_dia(cuenta_id, year, month, day)
        elif year is not None and month is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_mes(cuenta_id, year, month)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_mes(cuenta_id, year, month)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_mes(cuenta_id, year, month)
        elif year is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_anio(cuenta_id, year)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_anio(cuenta_id, year)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_anio(cuenta_id, year)
        else:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos(cuenta_id)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto(cuenta_id)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso(cuenta_id)
    else:
        resumen = {'cuentas': [], 'cuenta': None, 'categorias': [], 'total_ingresos': 0, 'total_gastos': 0}
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []
        grafico_ingresos_categoria = []

    # PRINTS DE DEBUG (agrega estos para saber qué tipo de datos tienes)
    print('--- DEBUG DASHBOARD ---')
    print('Resumen:', resumen)
    if 'categorias' in resumen:
        for i, cat in enumerate(resumen['categorias']):
            print(f"categorias[{i}]: type={type(cat)}, value={cat}")
            if hasattr(cat, 'tipo'):
                print(f"   tipo={cat.tipo}, type={type(cat.tipo)}")
            if isinstance(cat, dict):
                print(f"   dict tipo={cat.get('tipo')}, type={type(cat.get('tipo'))}")

    print('Datos gráfico gastos categoría:', grafico_gastos_categoria)
    for i, dato in enumerate(grafico_gastos_categoria):
        print(f"gastos_categoria[{i}]: type={type(dato)}, value={dato}")

    print('Datos gráfico ingresos categoría:', grafico_ingresos_categoria)
    for i, dato in enumerate(grafico_ingresos_categoria):
        print(f"ingresos_categoria[{i}]: type={type(dato)}, value={dato}")

    # Serialización (ajusta según tus modelos)
    def serialize_usuario(usuario):
        return {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            # agrega otros campos si los necesitas
        }
    
    resumen_dict = {
        'cuentas': [c.to_dict() for c in resumen.get('cuentas', [])],
        'cuenta': resumen['cuenta'].to_dict() if resumen.get('cuenta') else None,
        'categorias': [
            {
                'categoria': cat['categoria'].to_dict() if hasattr(cat['categoria'], 'to_dict') else cat['categoria'],
                'transacciones': cat.get('transacciones', [])
            }
            for cat in resumen.get('categorias', [])
        ],
        'total_ingresos': resumen.get('total_ingresos', 0),
        'total_gastos': resumen.get('total_gastos', 0),
    }

    return jsonify({
        'success': True,
        'usuario': serialize_usuario(usuario),
        'datos_grafico': datos_grafico,
        'datos_grafico_categoria': grafico_gastos_categoria,
        'datos_grafico_categoria_ingreso': grafico_ingresos_categoria,
        'resumen': resumen_dict,
        'notificaciones': [
            {'id': n.id, 'mensaje': n.mensaje, 'leido': n.leido}
            for n in notificaciones
        ]
    })
