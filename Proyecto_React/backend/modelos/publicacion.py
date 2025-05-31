from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'))

    # Relaciones
    usuario = relationship("Usuario", back_populates="publicaciones")
    comentarios = relationship("Comentario", back_populates="publicacion", cascade="all, delete-orphan")
    suscripciones = relationship("Suscripcion", back_populates="publicacion", cascade="all, delete-orphan")

    def to_dict(self, include_comentarios=False, include_usuario_nombre=False):
        data = {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "usuario_id": self.usuario_id,
        }
        if include_comentarios:
            data["comentarios"] = [c.to_dict() for c in self.comentarios]
        if include_usuario_nombre:
            data["usuario_nombre"] = self.usuario.nombre if self.usuario else None
        return data
