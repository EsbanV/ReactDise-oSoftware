import logging
from modelos.cuenta_bancaria import CuentaBancaria
from utilidades.validaciones import validar_nombre, validar_monto

class CuentaBancariaServicio:

    def __init__(self, repositorio, categoria_servicio):
        self.repositorio = repositorio
        self.categoria_servicio = categoria_servicio

    CATEGORIAS_GASTO_PREDEFINIDAS = ["Alimentación", "Transporte", "Entretenimiento", "Salud"]
    CATEGORIAS_INGRESO_PREDEFINIDAS = ["Salario", "Inversiones"]
    
    def crear_cuenta(self, nombre, saldo_inicial, usuario_id):

        cuentas = self.repositorio.obtener_con_filtro(CuentaBancaria, [CuentaBancaria.usuario_id == usuario_id])
        if len(cuentas) > 5:
            raise ValueError("No puedes tener más de 5 cuentas bancarias.")

        if not validar_nombre(nombre):
            raise ValueError("Nombre de cuenta inválido")

        if not validar_monto(saldo_inicial):
            raise ValueError("Saldo inicial debe ser un número positivo")

        nueva_cuenta = CuentaBancaria(nombre=nombre, saldo=saldo_inicial, usuario_id=usuario_id)
        try:
            self.repositorio.agregar(nueva_cuenta)

            for nombre_categoria in CuentaBancariaServicio.CATEGORIAS_GASTO_PREDEFINIDAS:
                presupuesto=None
                categoria = self.categoria_servicio.crear_categoria(nombre_categoria, "GASTO", presupuesto, nueva_cuenta.id)
                self.repositorio.agregar(categoria)

            for nombre_categoria in CuentaBancariaServicio.CATEGORIAS_INGRESO_PREDEFINIDAS:
                presupuesto=None
                categoria = self.categoria_servicio.crear_categoria(nombre_categoria, "INGRESO", presupuesto, nueva_cuenta.id)
                self.repositorio.agregar(categoria)

            logging.info("Cuenta bancaria creada correctamente: %s", nueva_cuenta.nombre)
        except Exception as e:
            logging.error("Error al crear cuenta bancaria para usuario %s: %s", usuario_id, e)
            raise e
        return nueva_cuenta
    
    def obtener_cuentas(self, usuario_id):
        cuentas = self.repositorio.obtener_con_filtro(CuentaBancaria, [CuentaBancaria.usuario_id == usuario_id])
        logging.info("Obtenidas %d cuentas para el usuario %s", len(cuentas), usuario_id)
        return cuentas
    
    def obtener_cuenta_por_id(self, cuenta_id):
        cuenta = self.repositorio.obtener_por_id(CuentaBancaria, cuenta_id)
        if cuenta:
            logging.info("Cuenta bancaria encontrada: ID %s, Nombre %s", cuenta_id, cuenta.nombre)
        else:
            logging.warning("Cuenta bancaria no encontrada: ID %s", cuenta_id)
        return cuenta
    
    def obtener_primer_cuenta(self, usuario_id):
        cuentas = self.obtener_cuentas(usuario_id)
        if cuentas:
            logging.info("Primera cuenta bancaria obtenida: ID %s", cuentas[0].id)
            return cuentas[0]
        else:
            logging.warning("No se encontraron cuentas para el usuario %s", usuario_id)
            return None

    def actualizar_cuenta(self, cuenta_id, nombre=None, saldo=None):
        cuenta = CuentaBancaria.query.get(cuenta_id)
        if not cuenta:
            logging.warning("No se pudo actualizar, cuenta no encontrada: ID %s", cuenta_id)
            return None

        if nombre is not None:
            cuenta.nombre = nombre
        if saldo is not None:
            cuenta.saldo = saldo

        try:
            self.repositorio.actualizar()
            logging.info("Cuenta bancaria actualizada: ID %s", cuenta_id)
        except Exception as e:
            logging.error("Error al actualizar la cuenta ID %s: %s", cuenta_id, e)
            raise e

        return cuenta

    def eliminar_cuenta(self, cuenta_id):
        cuenta = CuentaBancaria.query.get(cuenta_id)
        if not cuenta:
            logging.warning("Intento de eliminar cuenta inexistente: ID %s", cuenta_id)
            return None

        try:
            self.repositorio.eliminar(cuenta)
            logging.info("Cuenta bancaria eliminada: ID %s", cuenta_id)
        except Exception as e:
            logging.error("Error al eliminar cuenta bancaria ID %s: %s", cuenta_id, e)
            raise e

        return cuenta
