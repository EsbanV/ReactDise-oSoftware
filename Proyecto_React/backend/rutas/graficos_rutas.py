from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
from functools import wraps

graficos_rutas = Blueprint('graficos_rutas', __name__)

@graficos_rutas.route('/', methods=['GET'])
def obtener_datos_graficos_api():
    usuario_id = session.get("usuario_id")
    cuenta_id = request.args.get('cuenta_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

    # Validación de cuenta
    if cuenta_id:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        if cuenta is None or cuenta.usuario_id != usuario_id:
            return jsonify({"error": "Cuenta no encontrada o no pertenece al usuario"}), 403

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
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []
        grafico_ingresos_categoria = []

    return jsonify({
        "datos_grafico": datos_grafico,
        "datos_grafico_categoria": grafico_gastos_categoria,
        "datos_grafico_categoria_ingreso": grafico_ingresos_categoria,
    })
