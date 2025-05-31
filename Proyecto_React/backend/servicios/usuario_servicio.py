import logging
from modelos.usuario import Usuario
from utilidades.seguridad import encriptar_contrasena, verificar_contrasena
from utilidades.validaciones import validar_email, validar_password
from utilidades.validaciones_macro import validar_datos_usuario
from modelos.categoria import TipoCategoria
from modelos.transaccion import Transaccion
from sqlalchemy.orm import joinedload
from builder.usuario_builder import UsuarioBuilder

class UsuarioServicio:

    def __init__(self, transaccion_repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio):
        self.transaccion_repositorio = transaccion_repositorio
        self.cuenta_bancaria_servicio = cuenta_bancaria_servicio
        self.categoria_servicio = categoria_servicio
        self.transaccion_servicio = transaccion_servicio

    
    def obtener_usuario_activo(self, usuario_id):
        return self.transaccion_repositorio.obtener_unico_con_filtro(Usuario, [Usuario.id == usuario_id, Usuario.activo == True])

    
    def registrar_usuario(self, nombre, correo, contrasena):

        validar_datos_usuario(nombre, correo, contrasena)

        if self.transaccion_repositorio.obtener_con_filtro(Usuario, [Usuario.correo == correo]):
            logging.error("El correo ya está en uso: %s", correo)
            raise ValueError("El correo ya está en uso")
        
        contrasena_encriptada = encriptar_contrasena(contrasena)

        usuario = (
                    UsuarioBuilder()
                    .nombre(nombre)
                    .correo(correo)
                    .contrasena(contrasena_encriptada)
                    .activo(True)
                    .build()
                  )
        try:
            self.transaccion_repositorio.agregar(usuario)
            logging.info("Usuario creado correctamente: %s", correo)
        except Exception as e:
            logging.error("Error al crear usuario %s: %s", correo, e)
            raise e
        return usuario

    
    def iniciar_sesion(self, correo, contrasena):
        usuario = self.transaccion_repositorio.obtener_unico_con_filtro(Usuario, [Usuario.correo == correo, Usuario.activo == True])
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            logging.info("Inicio de sesión exitoso para: %s", correo)
            return usuario
        else:
            logging.error("Credenciales inválidas para: %s", correo)
            raise ValueError("Credenciales inválidas")

    
    def actualizar_usuario(self, usuario_id, nombre=None, correo=None, contrasena=None):
        usuario = self.transaccion_repositorio.obtener_unico_con_filtro(Usuario, [Usuario.id == usuario_id, Usuario.activo == True])
        if not usuario:
            logging.warning("Usuario no encontrado para actualizar: ID %s", usuario_id)
            return None

        if nombre:
            usuario.nombre = nombre
        if correo:
            if not validar_email(correo):
                raise ValueError("Email inválido")
            usuario.correo = correo
        if contrasena:
            if not validar_password(contrasena):
                raise ValueError("Contraseña inválida")
            usuario.contrasena = encriptar_contrasena(contrasena)

        try:
            self.transaccion_repositorio.actualizar(usuario)
            logging.info("Usuario actualizado: ID %s", usuario_id)
        except Exception as e:
            logging.error("Error al actualizar usuario %s: %s", usuario_id, e)
            raise e
        return usuario

    
    def eliminar_usuario(self, usuario_id):
        usuario = self.transaccion_repositorio.obtener_por_id(Usuario, usuario_id)
        if usuario:
            try:
                usuario.activo = False
                self.transaccion_repositorio.actualizar(usuario)
                logging.info("Usuario eliminado: ID %s", usuario_id)
            except Exception as e:
                logging.error("Error al eliminar usuario %s: %s", usuario_id, e)
                raise e
            return True
        logging.warning("Intento de eliminar usuario inexistente: ID %s", usuario_id)
        return False


    
    def datos_usuario(self, usuario_id):
        usuario = self.transaccion_repositorio.obtener_unico_con_filtro(Usuario, [Usuario.id == usuario_id, Usuario.activo == True])
        if usuario:
            return usuario
        else:
            logging.warning("Usuario no encontrado: ID %s", usuario_id)
            raise ValueError("Usuario no encontrado")

    
    def obtener_resumen(self, usuario_id, cuenta_id=None):
        usuario = self.transaccion_repositorio.obtener_unico_con_filtro(Usuario, [Usuario.id == usuario_id, Usuario.activo == True])
        if not usuario:
            raise ValueError("Usuario no encontrado o desactivado")

        cuentas = self.cuenta_bancaria_servicio.obtener_cuentas(usuario_id)
        if not cuentas:
            return {
                "cuenta": None,
                "cuentas": [],
                "total_ingresos": 0.0,
                "total_gastos": 0.0,
                "categorias": []
            }

        cuenta = next((c for c in cuentas if c.id == cuenta_id), cuentas[0])

        # Usar el servicio de transacciones (que a su vez usa el repo específico)
        transacciones = self.transaccion_servicio.obtener_transacciones_por_cuenta_con_categoria(cuenta.id)

        total_ingresos = sum(
            t.monto for t in transacciones if t.categoria and t.categoria.tipo == TipoCategoria.INGRESO
        )
        total_gastos = sum(
            -t.monto for t in transacciones if t.categoria and t.categoria.tipo == TipoCategoria.GASTO
        )

        categorias_raw = self.categoria_servicio.obtener_categorias(cuenta.id)
        categorias = [
            {
                "categoria": cat,
                "transacciones": self.transaccion_servicio.obtener_por_categoria_y_cuenta(cuenta.id, cat.id)
            }
            for cat in categorias_raw
        ]

        return {
            "cuenta": cuenta,
            "cuentas": cuentas,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "categorias": categorias
        }
