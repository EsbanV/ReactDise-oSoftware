from modelos.categoria import Categoria, TipoCategoria
from modelos.transaccion import Transaccion
from modelos.cuenta_bancaria import CuentaBancaria
from datetime import datetime, timedelta

class GraficoServicio:

    def __init__(self, repositorio):
        self.repositorio = repositorio

    # --------- RANGOS DE FECHA ---------
    def _rango_mes(self, year, month):
        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)
        return fecha_inicio, fecha_fin

    def _rango_anio(self, year):
        return datetime(year, 1, 1), datetime(year + 1, 1, 1)

    def _rango_dia(self, year, month, day):
        fecha_inicio = datetime(year, month, day)
        fecha_fin = fecha_inicio + timedelta(days=1)
        return fecha_inicio, fecha_fin

    # --------- DATOS CRUDOS (Balance general) ---------
    def obtener_datos_crudos(self, cuenta_id):
        return self._obtener_datos_crudos_en_rango(cuenta_id)

    def obtener_datos_crudos_por_anio(self, cuenta_id, year):
        fecha_inicio, fecha_fin = self._rango_anio(year)
        return self._obtener_datos_crudos_en_rango(cuenta_id, fecha_inicio, fecha_fin)

    def obtener_datos_crudos_por_mes(self, cuenta_id, year, month):
        fecha_inicio, fecha_fin = self._rango_mes(year, month)
        return self._obtener_datos_crudos_en_rango(cuenta_id, fecha_inicio, fecha_fin)

    def obtener_datos_crudos_por_dia(self, cuenta_id, year, month, day):
        fecha_inicio, fecha_fin = self._rango_dia(year, month, day)
        return self._obtener_datos_crudos_en_rango(cuenta_id, fecha_inicio, fecha_fin)

    def _obtener_datos_crudos_en_rango(self, cuenta_id, fecha_inicio=None, fecha_fin=None):
        cuenta = self.repositorio.obtener_por_id(CuentaBancaria, cuenta_id)
        if not cuenta:
            return {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}

        filtros = [Transaccion.cuenta_bancaria_id == cuenta.id]
        if fecha_inicio and fecha_fin:
            filtros += [Transaccion.fecha >= fecha_inicio, Transaccion.fecha < fecha_fin]

        transacciones = self.repositorio.obtener_con_filtro(Transaccion, filtros)
        ingresos, gastos = 0, 0
        for t in transacciones:
            categoria = self.repositorio.obtener_por_id(Categoria, t.categoria_id)
            t.categoria = categoria
            if categoria:
                if categoria.tipo == TipoCategoria.INGRESO:
                    ingresos += abs(t.monto)
                elif categoria.tipo == TipoCategoria.GASTO:
                    gastos += abs(t.monto)
                else:
                    if t.monto > 0: ingresos += t.monto
                    else: gastos += abs(t.monto)
            else:
                if t.monto > 0: ingresos += t.monto
                else: gastos += abs(t.monto)
        return {
            'ingresos': round(ingresos, 2),
            'gastos': round(gastos, 2),
            'balance_neto': round(ingresos - gastos, 2)
        }

    # --------- DATOS POR CATEGORÍA ---------
    def obtener_datos_categorias_gasto(self, cuenta_id):
        return self._obtener_categorias_en_rango(cuenta_id, tipo=TipoCategoria.GASTO)

    def obtener_datos_categorias_gasto_por_anio(self, cuenta_id, year):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.GASTO, *self._rango_anio(year))

    def obtener_datos_categorias_gasto_por_mes(self, cuenta_id, year, month):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.GASTO, *self._rango_mes(year, month))

    def obtener_datos_categorias_gasto_por_dia(self, cuenta_id, year, month, day):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.GASTO, *self._rango_dia(year, month, day))

    def obtener_datos_categorias_ingreso(self, cuenta_id):
        return self._obtener_categorias_en_rango(cuenta_id, tipo=TipoCategoria.INGRESO)

    def obtener_datos_categorias_ingreso_por_anio(self, cuenta_id, year):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.INGRESO, *self._rango_anio(year))

    def obtener_datos_categorias_ingreso_por_mes(self, cuenta_id, year, month):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.INGRESO, *self._rango_mes(year, month))

    def obtener_datos_categorias_ingreso_por_dia(self, cuenta_id, year, month, day):
        return self._obtener_categorias_rango_fecha(cuenta_id, TipoCategoria.INGRESO, *self._rango_dia(year, month, day))

    # --------- HELPERS GENERALES ---------
    def _obtener_categorias_en_rango(self, cuenta_id, tipo):
        categorias = self.repositorio.obtener_con_filtro(
            Categoria, [Categoria.cuenta_id == cuenta_id, Categoria.tipo == tipo]
        )
        datos = []
        for categoria in categorias:
            transacciones = self.repositorio.obtener_con_filtro(
                Transaccion, [Transaccion.categoria_id == categoria.id]
            )
            monto_total = sum(abs(t.monto) for t in transacciones)
            if monto_total > 0:
                datos.append({
                    'nombre': categoria.nombre or "Sin Nombre",
                    'tipo': categoria.tipo.value,
                    'total': monto_total or 0
                })
        return datos

    def _obtener_categorias_rango_fecha(self, cuenta_id, tipo, fecha_inicio, fecha_fin):
        categorias = self.repositorio.obtener_con_filtro(
            Categoria, [Categoria.cuenta_id == cuenta_id, Categoria.tipo == tipo]
        )
        datos = []
        for categoria in categorias:
            transacciones = self.repositorio.obtener_con_filtro(
                Transaccion, [
                    Transaccion.categoria_id == categoria.id,
                    Transaccion.fecha >= fecha_inicio,
                    Transaccion.fecha < fecha_fin
                ]
            )
            monto_total = sum(abs(t.monto) for t in transacciones)
            if monto_total > 0:
                datos.append({
                    'nombre': categoria.nombre or "Sin Nombre",
                    'tipo': categoria.tipo.value,
                    'total': monto_total or 0
                })
        return datos
