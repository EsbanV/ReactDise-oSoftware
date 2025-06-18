from servicios.base_datos import ServicioBaseDatos
from modelos.publicacion import Publicacion

class PublicacionRepositorio(ServicioBaseDatos):
    
    def obtener_publicaciones(self, limit=5, offset=0):
        print(f"Repositorio: limit={limit}, offset={offset}")
        query = self.session.query(Publicacion).order_by(Publicacion.fecha_creacion.desc())
        total = query.count()
        publicaciones = query.limit(limit).offset(offset).all()
        return publicaciones, total