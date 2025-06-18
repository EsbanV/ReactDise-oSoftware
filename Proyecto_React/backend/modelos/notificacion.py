from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True)
    mensaje = Column(String(255), nullable=False)
    leida = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'))
    usuario = relationship("Usuario", back_populates="notificaciones")

    def __repr__(self):
        return f'<Notificación {self.mensaje} para Usuario {self.usuario_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "leida": self.leida,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "usuario_id": self.usuario_id,
        }