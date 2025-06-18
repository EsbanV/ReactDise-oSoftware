from configuracion.extensiones import db

class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'
    id = db.Column(db.Integer, primary_key=True)
    monto_asignado = db.Column(db.Float, nullable=False)
    monto_gastado = db.Column(db.Float, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='CASCADE'), nullable=False)

    categoria = db.relationship("Categoria", back_populates="presupuesto", passive_deletes=True)

    def __repr__(self):
        return f'<Presupuesto {self.id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "monto_asignado": self.monto_asignado,
            "monto_gastado": self.monto_gastado,
            "categoria_id": self.categoria_id,
        }