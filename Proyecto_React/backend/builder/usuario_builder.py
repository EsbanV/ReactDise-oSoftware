from modelos.usuario import Usuario
from utilidades.seguridad import encriptar_contrasena

class UsuarioBuilder:
    def __init__(self):
        self._atributos = {}

    def nombre(self, nombre):
        self._atributos['nombre'] = nombre
        return self

    def correo(self, correo):
        self._atributos['correo'] = correo
        return self

    def contrasena(self, contrasena):
        self._atributos['contrasena'] = contrasena
        return self

    def activo(self, activo=True):
        self._atributos['activo'] = activo
        return self

    def build(self):
        requeridos = ['nombre', 'correo', 'contrasena']
        for campo in requeridos:
            if campo not in self._atributos:
                raise ValueError(f"El campo obligatorio '{campo}' falta en la creación del usuario")
        return Usuario(**self._atributos)
