import logging
from modelos.presupuesto import Presupuesto

class PresupuestoServicio:

    def __init__(self, repositorio):
        self.repositorio = repositorio

    
    
    def asignar_presupuesto(self, categoria_id, monto_asignado):
        presupuesto = self.repositorio.obtener_unico_con_filtro(
            Presupuesto,
            [Presupuesto.categoria_id == categoria_id]
        )
        try:
            if presupuesto:
                presupuesto.monto_asignado = monto_asignado
                self.repositorio.actualizar()
                logging.info("Presupuesto actualizado para categoría %s: nuevo monto %s", categoria_id, monto_asignado)
            else:
                presupuesto = Presupuesto(categoria_id=categoria_id, monto_asignado=monto_asignado)
                self.repositorio.agregar(presupuesto)
                logging.info("Nuevo presupuesto asignado para categoría %s: monto %s", categoria_id, monto_asignado)
        except Exception as e:
            logging.error("Error al asignar presupuesto para categoría %s: %s", categoria_id, e)
            raise e

        return presupuesto


    
    def obtener_presupuesto(self, categoria_id):
        presupuesto = self.repositorio.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == categoria_id])
        if presupuesto:
            logging.info("Presupuesto obtenido para categoría %s", categoria_id)
        else:
            logging.info("No se encontró presupuesto para la categoría %s", categoria_id)
        return presupuesto

    
    def eliminar_presupuesto(self, presupuesto_id):
        presupuesto = Presupuesto.query.get(presupuesto_id)
        if presupuesto:
            try:
                self.repositorio.eliminar(presupuesto)
                logging.info("Presupuesto eliminado: ID %s", presupuesto_id)
            except Exception as e:
                logging.error("Error al eliminar presupuesto ID %s: %s", presupuesto_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar presupuesto inexistente: ID %s", presupuesto_id)
        return presupuesto
