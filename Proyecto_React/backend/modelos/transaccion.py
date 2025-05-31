from datetime import datetime
from configuracion.extensiones import db

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='CASCADE'), nullable=False)
    cuenta_bancaria_id = db.Column(db.Integer,db.ForeignKey('cuentas_bancarias.id', ondelete='CASCADE'), nullable=False)

    cuenta_bancaria = db.relationship("CuentaBancaria", back_populates="transacciones", passive_deletes=True)
    categoria = db.relationship("Categoria", back_populates="transacciones", passive_deletes=True)

    def __repr__(self):
        return f'<Transaccion {self.id}>'

    def to_dict(self, include_categoria_nombre=False):
        data = {
            "id": self.id,
            "monto": self.monto,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "categoria_id": self.categoria_id,
            "cuenta_bancaria_id": self.cuenta_bancaria_id,
        }
        if include_categoria_nombre:
            data["categoria_nombre"] = self.categoria.nombre if self.categoria else None
        return data