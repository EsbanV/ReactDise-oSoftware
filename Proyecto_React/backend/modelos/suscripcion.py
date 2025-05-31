# models.py (o donde agrupes tus modelos)
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'

    # Clave primaria compuesta
    usuario_id     = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id', ondelete='CASCADE'), primary_key=True)

    # Campos adicionales
    fecha           = Column(DateTime, default=datetime.utcnow)
    estado          = Column(String(20), default='activa')

    # Relaciones de navegación
    usuario     = relationship("Usuario",      back_populates="suscripciones")
    publicacion = relationship("Publicacion",  back_populates="suscripciones")

    def to_dict(self, include_nombres=False, include_publicacion_titulo=False):
        data = {
            "usuario_id": self.usuario_id,
            "publicacion_id": self.publicacion_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "estado": self.estado,
        }
        if include_nombres:
            data["usuario_nombre"] = self.usuario.nombre if self.usuario else None
        if include_publicacion_titulo:
            data["publicacion_titulo"] = self.publicacion.titulo if self.publicacion else None
        return data