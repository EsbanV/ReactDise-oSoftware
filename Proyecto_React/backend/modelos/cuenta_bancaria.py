from configuracion.extensiones import db

class CuentaBancaria(db.Model):
    __tablename__ = 'cuentas_bancarias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuarios.id', ondelete='CASCADE'),nullable=False)
    
    usuario = db.relationship("Usuario", back_populates="cuentas_bancarias", passive_deletes=True)
    categorias = db.relationship("Categoria", back_populates="cuenta_bancaria", passive_deletes=True)
    transacciones = db.relationship("Transaccion", back_populates="cuenta_bancaria", passive_deletes=True)

    def __repr__(self):
        return f'<CuentaBancaria {self.id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "saldo": self.saldo,
            "usuario_id": self.usuario_id,
        }