from modelos.categoria import Categoria, TipoCategoria

class CategoriaFactory:
    @staticmethod
    def crear_categoria(nombre, tipo, cuenta_id):
        if isinstance(tipo, str):
            tipo = tipo.lower()
            if tipo == "ingreso":
                tipo_enum = TipoCategoria.INGRESO
            elif tipo == "gasto":
                tipo_enum = TipoCategoria.GASTO
            else:
                raise ValueError("Tipo de categoría inválido")
        elif isinstance(tipo, TipoCategoria):
            tipo_enum = tipo
        else:
            raise ValueError("Tipo de categoría inválido")
        
        return Categoria(nombre=nombre, tipo=tipo_enum, cuenta_id=cuenta_id)
