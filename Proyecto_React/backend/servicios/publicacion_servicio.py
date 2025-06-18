from modelos.publicacion import Publicacion
from modelos.comentario import Comentario
from flask import abort
from better_profanity import profanity
from utilidades.validaciones_macro import cargar_palabras_ofensivas


profanity.load_censor_words()
cargar_palabras_ofensivas("configuracion/palabras_ofensivas.txt")

LIMITE_CARACTERES_PUBLICACION = 500
LIMITE_CARACTERES_TITULO = 100
class PublicacionService:

    def __init__(self, repositorio, publicacion_repositorio, usuario_servicio,comment_observers=None, publication_observers=None):
        self.repositorio = repositorio
        self.publicacion_repositorio = publicacion_repositorio
        self.usuario_servicio = usuario_servicio
        self.comment_observers = comment_observers or []
        self.publication_observers = publication_observers or []

    def comentario_valido(self, texto):
        return not profanity.contains_profanity(texto)
    
    
    def crear_publicacion(self, usuario_id: int, titulo: str, contenido: str) -> Publicacion:
        if len(contenido) > LIMITE_CARACTERES_PUBLICACION:
            raise ValueError(f"La publicación no puede superar los {LIMITE_CARACTERES_PUBLICACION} caracteres.")
        if len(titulo) > LIMITE_CARACTERES_TITULO:
            raise ValueError(f"El título no puede superar los {LIMITE_CARACTERES_TITULO} caracteres.")

        if not self.comentario_valido(contenido) or not self.comentario_valido(titulo):
            raise ValueError("La publicacion contiene palabras inapropiadas.")
        
        usuario = self.usuario_servicio.obtener_usuario_activo(usuario_id)
        if not usuario:
            abort(400, description="El usuario está desactivado")

        publicacion = Publicacion(titulo=titulo, contenido=contenido, usuario_id=usuario_id)
        self.repositorio.agregar(publicacion)

        texto = f"{publicacion.usuario.nombre} acaba de publicar «{publicacion.titulo}»"
        print("[SERVICIO] Notificando observers de comentario")
        for observer in self.publication_observers:  # <-- cambio aquí
            print(f"[SERVICIO] Enviando a observer: {observer}")
            observer.update(publicacion, evento='new_post', mensaje={'mensaje': texto})

        return publicacion
    
    
    def obtener_publicaciones(self, limit, offset):
        return self.publicacion_repositorio.obtener_publicaciones(limit, offset)


    
    def agregar_comentario(self, publicacion_id: int, usuario_id: int, contenido: str):
        print("[SERVICIO] agregar_comentario ejecutado")
        if len(contenido) > LIMITE_CARACTERES_PUBLICACION:
            raise ValueError(f"La publicación no puede superar los {LIMITE_CARACTERES_PUBLICACION} caracteres.")
        if not self.comentario_valido(contenido):
            raise ValueError("El comentario contiene palabras inapropiadas.")

        publicacion = self.repositorio.obtener_por_id(Publicacion, publicacion_id)
        if not publicacion:
            abort(404, description="Publicación no encontrada")

        usuario = self.usuario_servicio.obtener_usuario_activo(usuario_id)
        comentario = Comentario(contenido=contenido, usuario_id=usuario_id, publicacion_id=publicacion_id)
        try:
            self.repositorio.agregar(comentario)
            texto = f"{usuario.nombre} comentó en «{publicacion.titulo}»"
            for obs in self.comment_observers:  # <-- cambio aquí
                obs.update(publicacion, evento='comment', mensaje={'mensaje': texto})
        except Exception:
            raise

        return comentario
    
    
    def obtener_publicacion_o_404(self, publicacion_id: int):
        publicacion = self.repositorio.obtener_por_id(Publicacion, publicacion_id)
        if not publicacion:
            abort(404, description="Publicación no encontrada")
        return publicacion
