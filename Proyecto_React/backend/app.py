from utilidades.seguridad import generar_token_csrf
from configuracion.configuracion import crear_app
from utilidades.logging import init_logging

from servicios.base_datos import ServicioBaseDatos
from servicios.usuario_servicio import UsuarioServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.autor_servicio import AutorService
from servicios.notificacion_servicio import NotificacionService
from servicios.grafico_servicio import GraficoServicio
from servicios.publicacion_servicio import PublicacionService
from servicios.transaccion_base_datos import TransaccionRepositorio
from servicios.publicacion_base_datos import PublicacionRepositorio
from servicios.exportacion_servicio import ExportacionServicio
from observers.observer import NotificationObserver
from configuracion.configuracion import db
from flask_cors import CORS

from servicios.FinanzasFacade import (UsuarioFacade, CuentaBancariaFacade, CategoriaFacade,
                                      PresupuestoFacade, TransaccionFacade, 
                                      GraficoFacade, ComunidadFacade, ExportacionFacade
                                     )

def create_app():
    app = crear_app()
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173"],
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    )
    repositorio = ServicioBaseDatos(db.session)
    transaccion_repositorio = TransaccionRepositorio(db.session)
    publicacion_repositorio = PublicacionRepositorio(db.session)

    observer = NotificationObserver(repositorio)
    presupuesto_servicio = PresupuestoServicio(repositorio)
    categoria_servicio = CategoriaServicio(repositorio, presupuesto_servicio)
    cuenta_bancaria_servicio = CuentaBancariaServicio(repositorio, categoria_servicio)
    transaccion_servicio = TransaccionServicio(transaccion_repositorio, categoria_servicio)
    usuario_servicio = UsuarioServicio(transaccion_repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio)

    autor_servicio = AutorService(repositorio, usuario_servicio, confirmation_observers = [observer], author_observers = [observer])
    publicacion_servicio = PublicacionService(repositorio, publicacion_repositorio, usuario_servicio, comment_observers = [observer], publication_observers = [observer])

    grafico_servicio = GraficoServicio(repositorio)
    notificacion_servicio = NotificacionService(repositorio)
    exportacion_servicio = ExportacionServicio(transaccion_repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio)

    
    app.repositorio = repositorio
    app.usuario_facade = UsuarioFacade(usuario_servicio)
    app.cuenta_bancaria_facade = CuentaBancariaFacade(cuenta_bancaria_servicio)
    app.categoria_facade = CategoriaFacade(categoria_servicio)
    app.presupuesto_facade = PresupuestoFacade(presupuesto_servicio)
    app.transaccion_facade = TransaccionFacade(transaccion_servicio)
    app.grafico_facade = GraficoFacade(grafico_servicio)
    app.comunidad_facade = ComunidadFacade(autor_servicio, publicacion_servicio, notificacion_servicio)
    app.exportacion_facade = ExportacionFacade(exportacion_servicio)

    from rutas.cuenta_bancaria_rutas import cuenta_rutas
    from rutas.categoria_rutas import categoria_rutas
    from rutas.presupuesto_rutas import presupuesto_rutas
    from rutas.transaccion_rutas import transaccion_rutas
    from rutas.usuario_rutas import usuario_rutas
    from rutas.dashboard_rutas import dashboard_rutas
    from rutas.graficos_rutas import graficos_rutas
    from rutas.autor_rutas import autor_rutas
    from rutas.publicacion_rutas import publicacion_rutas
    from rutas.notificacion_rutas import notificacion_rutas
    from rutas.exportacion_rutas import exportacion_rutas

    app.register_blueprint(graficos_rutas, url_prefix='/api/graficos')
    app.register_blueprint(cuenta_rutas, url_prefix='/api/cuentas')
    app.register_blueprint(categoria_rutas, url_prefix='/api/categorias')
    app.register_blueprint(presupuesto_rutas, url_prefix='/api/presupuestos')
    app.register_blueprint(usuario_rutas, url_prefix='/api/usuarios')
    app.register_blueprint(transaccion_rutas, url_prefix='/api/transacciones')
    app.register_blueprint(exportacion_rutas, url_prefix='/api/exportacion')
    app.register_blueprint(publicacion_rutas, url_prefix='/api/publicaciones')
    app.register_blueprint(autor_rutas, url_prefix='/api/autores')
    app.register_blueprint(notificacion_rutas, url_prefix='/api/notificaciones')
    app.register_blueprint(dashboard_rutas, url_prefix='/api/dashboard')


    init_logging(app)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generar_token_csrf)

    return app

if __name__ == '__main__':
    app = create_app()
    (app.run(debug=True))
        
