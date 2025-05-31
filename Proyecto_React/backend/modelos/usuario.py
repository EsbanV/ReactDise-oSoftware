from configuracion.extensiones import db
from sqlalchemy.orm import relationship
from modelos.suscripcion import Suscripcion

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    
    cuentas_bancarias = relationship("CuentaBancaria", back_populates="usuario", passive_deletes=True)
    comentarios = relationship("Comentario", back_populates="usuario", passive_deletes=True)
    notificaciones = relationship("Notificacion", back_populates="usuario", passive_deletes=True)
    publicaciones = relationship("Publicacion", back_populates="usuario", passive_deletes=True)
    suscripciones = relationship("Suscripcion", back_populates="usuario", cascade="all, delete-orphan")

    siguiendo = relationship("SuscripcionAutor", foreign_keys="[SuscripcionAutor.subscriber_id]", back_populates="suscriptor", cascade="all, delete-orphan")
    seguidores = relationship("SuscripcionAutor", foreign_keys="[SuscripcionAutor.autor_id]", back_populates="autor", cascade="all, delete-orphan")


    def __repr__(self):
        return f'<Usuario {self.id} - {self.nombre}>'
    
    def to_dict(self, include_email=True):
        """
        Devuelve los datos básicos del usuario.
        No expone la contraseña ni relaciones por defecto.
        """
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "activo": self.activo,
        }
        if include_email:
            data["correo"] = self.correo
        # Si quieres agregar listas de relaciones, puedes hacerlo opcionalmente aquí.
        # Ejemplo:
        # data["cuentas_bancarias"] = [c.to_dict() for c in self.cuentas_bancarias]
        return data