from flask import abort
from modelos.suscripcion_autor import SuscripcionAutor


class AutorService:

    def __init__(self, repositorio, usuario_servicio, confirmation_observers=None, author_observers=None):
        self.repositorio = repositorio
        self.usuario_servicio = usuario_servicio
        self.confirmation_observers = confirmation_observers or []
        self.author_observers = author_observers or []

    def suscribirse_autor(self, subscriber_id: int, autor_id: int):
        if subscriber_id == autor_id:
            abort(400, "No puedes suscribirte a ti mismo")
        suscripcion = SuscripcionAutor.query.get((subscriber_id, autor_id))
        if suscripcion:
            return suscripcion
        
        suscriptor = self.usuario_servicio.obtener_usuario_activo(subscriber_id)
        autor = self.usuario_servicio.obtener_usuario_activo(autor_id)

        suscripcion = SuscripcionAutor(subscriber_id=subscriber_id, autor_id=autor_id)
        self.repositorio.agregar(suscripcion)

        texto_autor = f"{suscriptor.nombre} te ha seguido"
        for obs in self.author_observers:
            obs.update(
                subject=autor,
                evento='new_subscription_author',
                mensaje={'mensaje': texto_autor}
            )

        texto_subs = f"Te has suscrito a {autor.nombre}"
        for obs in self.confirmation_observers:
            obs.update(
                subject=suscriptor,
                evento='new_subscription_confirmation',
                mensaje={
                    'mensaje': texto_subs,
                    'target_user_id': suscriptor.id
                }
            )


        return suscripcion

    
    def desuscribirse_autor(self, subscriber_id: int, autor_id: int):

        suscripcion = SuscripcionAutor.query.get((subscriber_id, autor_id))
        if not suscripcion:
            abort(400, "No estabas suscrito a este autor")

        self.repositorio.eliminar(suscripcion)
        return