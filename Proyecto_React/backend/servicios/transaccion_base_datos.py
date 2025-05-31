from servicios.base_datos import ServicioBaseDatos
from modelos import Transaccion, Categoria
from sqlalchemy.orm import joinedload

class TransaccionRepositorio(ServicioBaseDatos):
    def obtener_transacciones_con_categoria(self, cuenta_id):
        return (
            self.session.query(Transaccion)
            .join(Categoria)
            .filter(Transaccion.cuenta_bancaria_id == cuenta_id)
            .all()
        )
    
    def obtener_por_cuenta_con_categoria(self, cuenta_id):
            return (
                self.session.query(Transaccion)
                .options(joinedload(Transaccion.categoria))
                .filter_by(cuenta_bancaria_id=cuenta_id)
                .all()
            )