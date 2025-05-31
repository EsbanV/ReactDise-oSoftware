import logging
from modelos.categoria import Categoria
from modelos.cuenta_bancaria import CuentaBancaria
from utilidades.validaciones import validar_nombre
from factory.categoria_factory import CategoriaFactory
class CategoriaServicio:

    def __init__(self, repositorio, presupuesto_servicio):
        self.repositorio = repositorio
        self.presupuesto_servicio = presupuesto_servicio

    def crear_categoria(self, nombre, tipo, presupuesto, cuenta_id):
        categorias = self.repositorio.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta_id])
        if len(categorias) > 8:
            raise ValueError("No puedes tener más de 8 categorías en esta cuenta.")

        if not validar_nombre(nombre):
            raise ValueError("Nombre de categoría inválido")  

        if tipo == "INGRESO":
            if presupuesto:
                raise ValueError("No puedes asignar presupuesto a una categoria tipo ingreso")

        nueva_categoria = CategoriaFactory.crear_categoria(nombre=nombre, tipo=tipo, cuenta_id=cuenta_id)
        
        try:
            self.repositorio.agregar(nueva_categoria)
            logging.info("Categoría creada: %s para cuenta %s", nombre, tipo, cuenta_id)
        except Exception as e:
            logging.error("Error al crear categoría (%s) para cuenta %s: %s", nombre, tipo, cuenta_id, e)
            raise e
        
        if presupuesto:
            self.presupuesto_servicio.asignar_presupuesto(nueva_categoria.id, presupuesto)
        return nueva_categoria
    
    def obtener_categorias(self, cuenta_id):
        categorias = self.repositorio.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta_id])
        if categorias:
            logging.info("Obtenidas %d categorías para la cuenta %s", len(categorias), cuenta_id)
        else:
            return []
        return categorias
    
    def actualizar_categoria(self, categoria_id, nombre):
        if not validar_nombre(nombre):
            raise ValueError("Nombre de categoría inválido")

        categoria = self.repositorio.obtener_por_id(Categoria, categoria_id)
        if not categoria:
            logging.warning("Categoría no encontrada para actualizar: ID %s", categoria_id)
            return None

        old_name = categoria.nombre
        categoria.nombre = nombre
        try:
            self.repositorio.actualizar()
            logging.info("Categoría actualizada: ID %s, de '%s' a '%s'", categoria_id, old_name, nombre)
        except Exception as e:
            logging.error("Error al actualizar categoría ID %s: %s", categoria_id, e)
            raise e
        return categoria

    def eliminar_categoria(self, categoria_id):
        categoria = self.repositorio.obtener_por_id(Categoria, categoria_id)
        if not categoria:
            logging.warning("Intento de eliminar categoría inexistente: ID %s", categoria_id)
            return False

        try:
            self.repositorio.eliminar(categoria)
            logging.info("Categoría eliminada: ID %s", categoria_id)
            return True
        except Exception as e:
            logging.error("Error al eliminar categoría ID %s: %s", categoria_id, e)
            raise e

    def obtener_categorias_por_usuario(self, usuario_id):
        cuentas = self.repositorio.obtener_con_filtro(CuentaBancaria, [CuentaBancaria.usuario_id == usuario_id])
        categorias = []
        for cuenta in cuentas:
            categorias_cuenta = self.repositorio.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta.id])
            categorias.extend(categorias_cuenta)
        logging.info("Obtenidas %d categorías para el usuario %s", len(categorias), usuario_id)
        return categorias

    def obtener_categoria_por_id(self, categoria_id):
        categoria = self.repositorio.obtener_por_id(Categoria, categoria_id)
        if categoria:
            logging.info("Categoría encontrada: ID %s, Nombre %s", categoria_id, categoria.nombre)
        else:
            logging.warning("Categoría no encontrada: ID %s", categoria_id)
        return categoria
    
    def obtener_categorias_filtradas(self, cuenta_id, tipo=None):
        filtros = [Categoria.cuenta_id == cuenta_id]
        if tipo:
            filtros.append(Categoria.tipo == tipo)
        categorias = self.repositorio.obtener_con_filtro(Categoria, filtros)
        logging.info("Obtenidas %d categorías filtradas para la cuenta %s", len(categorias), cuenta_id)
        return categorias
