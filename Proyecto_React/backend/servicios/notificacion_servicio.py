from modelos.notificacion import Notificacion

class NotificacionService:

    def __init__(self, repositorio):
        self.repositorio = repositorio

    
    def obtener_notificaciones(self, usuario_id: int):
        return Notificacion.query.filter_by(usuario_id=usuario_id).order_by(Notificacion.fecha_creacion.desc()).all()

    
    def marcar_notificacion_leida(self, notificacion_id: int):
        notificacion = Notificacion.query.get_or_404(notificacion_id)
        notificacion.leida = True
        self.repositorio.agregar(notificacion)
        return notificacion
