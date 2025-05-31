class ServicioBaseDatos:
    def __init__(self, session):
        self.session = session

    def agregar(self, instancia):
        try:
            self.session.add(instancia)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def actualizar(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def eliminar(self, instancia):
        try:
            self.session.delete(instancia)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def obtener_todos(self, modelo):
        return self.session.query(modelo).all()

    def obtener_por_id(self, modelo, id_):
        return self.session.query(modelo).get(id_)

    def obtener_con_filtro(self, modelo, condiciones=None):
        condiciones = condiciones or []
        return self.session.query(modelo).filter(*condiciones).all()

    def obtener_unico_con_filtro(self, modelo, condiciones=None):
        condiciones = condiciones or []
        return self.session.query(modelo).filter(*condiciones).first()
