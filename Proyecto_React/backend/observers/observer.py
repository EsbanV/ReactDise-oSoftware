# services/observer.py (continúa)

from configuracion.extensiones import db
from observers.iObserver import Observer
from modelos.notificacion import Notificacion
from flask import current_app

class NotificationObserver(Observer):
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def update(self, subject, evento: str, mensaje: dict):
        print("[OBSERVER] update llamado")
        print(f"[OBSERVER] publicacion: {subject}, evento: {evento}, mensaje: {mensaje}")

        current_app.logger.debug(f"[NotificationObserver] evento={evento}, subject={subject}, mensaje={mensaje}")

        if evento == 'comment':
            targets = [subject.usuario_id]
            print(f"[OBSERVER] Usuarios a notificar: {targets}")
        elif evento == 'new_post':
            targets = [sa.subscriber_id for sa in subject.usuario.seguidores]

        elif evento == 'new_subscription_author':
            targets = [subject.id]

        elif evento == 'new_subscription_confirmation':
            targets = [mensaje['target_user_id']]
        else:
            return

        print(f"[OBSERVER] Notificación a guardar:")
        errores = []
        for uid in targets:
            noti = Notificacion(mensaje=mensaje['mensaje'], usuario_id=uid)
            try:
                self.repositorio.agregar(noti)
                print("[OBSERVER] Notificación guardada")
            except Exception as e:
                errores.append((uid, str(e)))

        if errores:
            for uid, err in errores:
                print(f"[ERROR] Falló notificación para usuario {uid}: {err}")