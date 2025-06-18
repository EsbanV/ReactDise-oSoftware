from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'))
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id', ondelete='CASCADE'))

    usuario = relationship("Usuario", back_populates="comentarios")
    publicacion = relationship("Publicacion", back_populates="comentarios")

    def __repr__(self):
        return f'<Comentario {self.id} - Publicación {self.publicacion_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "contenido": self.contenido,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "usuario_id": self.usuario_id,
            "publicacion_id": self.publicacion_id,
            "usuario_nombre": self.usuario.nombre if self.usuario else None,
        }