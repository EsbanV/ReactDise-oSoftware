from utilidades.validaciones import *
from better_profanity import profanity
import os

def validar_datos_usuario(nombre, correo, contrasena):
    if not validar_nombre(nombre):
        raise ValueError("Nombre inválido")
    if not validar_email(correo):
        raise ValueError("Email inválido")
    if not validar_password(contrasena):
        raise ValueError("Contraseña inválida")
    
def validar_datos_categoria(nombre, tipo, presupuesto):
    pass

def validar_datos_transaccion(servicio_base_datos, cuenta_id, categoria_id, monto, descripcion=None, fecha=None, validar_saldo=False):
    if not validar_monto(monto):
        raise ValueError("Monto inválido")

    if descripcion is not None and not validar_descripcion(descripcion):
        raise ValueError("Descripción inválida")

    cuenta = validar_existencia_cuenta(servicio_base_datos, cuenta_id)
    categoria = validar_existencia_categoria(servicio_base_datos, categoria_id)

    validar_categoria_pertenece_a_cuenta(categoria, cuenta)

    if fecha is not None:
        validar_fecha(fecha)

    return cuenta, categoria

def cargar_palabras_ofensivas(path_relativo="configuracion/palabras_ofensivas.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.abspath(os.path.join(base_dir, ".."))
    path_absoluto = os.path.join(proyecto_dir, path_relativo)
    print("Buscando archivo en:", path_absoluto)
    with open(path_absoluto, encoding="utf-8") as f:
        palabras = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    profanity.add_censor_words(palabras)