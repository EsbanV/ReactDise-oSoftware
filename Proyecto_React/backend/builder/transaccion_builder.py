from modelos.transaccion import Transaccion

class TransaccionBuilder:
    def __init__(self):
        self._atributos = {}

    def monto(self, monto):
        self._atributos['monto'] = monto
        return self

    def cuenta_bancaria_id(self, cuenta_id):
        self._atributos['cuenta_bancaria_id'] = cuenta_id
        return self

    def categoria_id(self, categoria_id):
        self._atributos['categoria_id'] = categoria_id
        return self

    def descripcion(self, descripcion):
        descripcion = descripcion.strip() if descripcion else None
        if not descripcion:
            descripcion = None
        self._atributos['descripcion'] = descripcion
        return self

    def fecha(self, fecha):
        self._atributos['fecha'] = fecha
        return self

    def build(self):
        requeridos = ['monto', 'cuenta_bancaria_id', 'categoria_id']
        for campo in requeridos:
            if campo not in self._atributos:
                raise ValueError(f"El campo obligatorio '{campo}' falta en la creación de la transacción")
        return Transaccion(**self._atributos)
