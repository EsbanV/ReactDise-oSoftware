# models/suscripcion_autor.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class SuscripcionAutor(db.Model):
    __tablename__ = 'suscripciones_autor'

    subscriber_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    autor_id      = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    fecha         = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    suscriptor = relationship("Usuario", foreign_keys=[subscriber_id], back_populates="siguiendo")
    autor      = relationship("Usuario", foreign_keys=[autor_id],      back_populates="seguidores")

    def to_dict(self, include_nombres=False):
        data = {
            "subscriber_id": self.subscriber_id,
            "autor_id": self.autor_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
        }
        if include_nombres:
            data["suscriptor_nombre"] = self.suscriptor.nombre if self.suscriptor else None
            data["autor_nombre"] = self.autor.nombre if self.autor else None
        return data