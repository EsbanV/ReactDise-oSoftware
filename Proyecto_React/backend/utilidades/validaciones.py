import re
from datetime import datetime, timedelta
from functools import wraps
from modelos import Usuario, CuentaBancaria, Categoria

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def validar_password(password, min_length=8):
    if len(password) < min_length:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def validar_nombre(nombre, min_length=2):
    if not nombre or len(nombre.strip()) < min_length:
        return False
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        return False
    return True

def validar_monto(monto):
    try:
        return float(monto) >= 0
    except (ValueError, TypeError):
        return False

def validar_monto_decorator(func):
    def wrapper(*args, **kwargs):
        monto = kwargs.get('monto')
        if not validar_monto(monto):
            raise ValueError("Monto inválido")
        return func(*args, **kwargs)
    return wrapper

def validar_descripcion(descripcion, max_length=200):
    if descripcion is None:
        return True  # O False si es obligatorio
    if len(descripcion.strip()) == 0:
        return False
    if len(descripcion) > max_length:
        return False
    return True

def validar_fecha(fecha, max_days_past=365, permitir_futuro=False):
    if not isinstance(fecha, datetime):
        return False
    hoy = datetime.utcnow()
    if not permitir_futuro and fecha > hoy:
        return False
    if fecha < hoy - timedelta(days=max_days_past):
        return False
    return True

def validar_categoria_pertenece_a_cuenta(categoria, cuenta):
    return categoria.cuenta_id == cuenta.id

def validar_unicidad_correo(servicio_base_datos, correo):
    return not servicio_base_datos.obtener_con_filtro(Usuario, [Usuario.correo == correo])

'''
def require_fields(*fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for field in fields:
                value = kwargs.get(field) or request.form.get(field)
                if value is None or value == '':
                    raise ValueError(f"El campo {field} es obligatorio.")
            return func(*args, **kwargs)
        return wrapper
    return decorator
'''
    
def validar_no_espacios(campo):
    return bool(campo and campo.strip())

def validar_existencia_cuenta(servicio_base_datos, cuenta_id):
    cuenta = servicio_base_datos.obtener_por_id(CuentaBancaria, cuenta_id)
    if not cuenta:
        raise ValueError("Cuenta bancaria no encontrada")
    return cuenta

def validar_existencia_categoria(servicio_base_datos, categoria_id):
    categoria = servicio_base_datos.obtener_por_id(Categoria, categoria_id)
    if not categoria:
        raise ValueError("Categoría no encontrada")
    return categoria

def alerta_saldo_insuficiente(saldo_final):
    if saldo_final <= 0:
        return "¡Atención! El saldo de esta cuenta ha quedado en cero o negativo. Revisa que tus datos sean correctos."
    return None

