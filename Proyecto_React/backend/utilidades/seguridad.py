from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def encriptar_contrasena(password):
    return generate_password_hash(password)

def verificar_contrasena(hashed_password, password):
   return check_password_hash(hashed_password, password)

def generar_token_csrf():

    return secrets.token_hex(16)
