import os
import importlib



ruta_actual = os.path.dirname(__file__)
modulos = [f[:-3] for f in os.listdir(ruta_actual) if f.endswith("_rutas.py")]

for modulo in modulos:
    importlib.import_module(f".{modulo}", package="rutas")
