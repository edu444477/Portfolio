from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt, bcrypt, init_extensions

from resources.auth_resource import RegisterResource, LoginResource
from resources.producto_resource import ProductoListResource, ProductoResource, CategoriaListResource, JuegoListResource
from resources.inventario_resource import InventarioUsuarioResource, VenderItemsResource
from resources.carrito_resource import CarritoResource, CarritoItemResource
from resources.pedido_resource import PedidoResource
from resources.perfil_resource import PerfilResource, CambiarContrasenaResource
from resources.deseo_resource import DeseoListResource, DeseoItemResource, DeseoIDsResource
from resources.intercambio_resource import IntercambioResource
from resources.newsletter_resource import NewsletterSubscribeResource

# Importar los modelos
from models import (
    Usuario, Empresa, Categoria, Juego, Producto,
    CarritoItem, DeseoItem, InventarioItem,
    Pedido, DetallePedido, Valoracion
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Habilitar CORS solo para desarrollo (localhost)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Para producción en PythonAnywhere, descomenta esta línea:
    # CORS(app, resources={r"/api/*": {"origins": "https://edufuengirola1.eu.pythonanywhere.com"}})

    # Inicializar extensiones centralizadamente
    init_extensions(app)

    # Registrar los recursos de la API
    register_api_resources(app)

    # Registrar Blueprints para vistas tradicionales
    # from .views import main_bp
    # app.register_blueprint(main_bp)

    # Filtro Jinja (si se renderizan plantillas HTML con Flask y es necesario formatear fechas/horas)
    # app.jinja_env.filters['strftime'] = strftime_filter

    return app

def register_api_resources(app):
    api = Api(app)

    # Aquí añadiremos los resources
    # Endpoints de Autenticación
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource,    '/api/auth/login')

    # Endpoints de Productos
    api.add_resource(ProductoListResource, '/api/productos')
    api.add_resource(ProductoResource,     '/api/productos/<int:producto_id>')

    # Endpoints para Filtros
    api.add_resource(CategoriaListResource, '/api/categorias')
    api.add_resource(JuegoListResource,     '/api/juegos')

    # Endpoints del usuario
    api.add_resource(InventarioUsuarioResource, '/api/inventario')
    api.add_resource(VenderItemsResource, '/api/inventario/vender')

    # Endpoints del carrito
    api.add_resource(CarritoResource, '/api/carrito')
    api.add_resource(CarritoItemResource, '/api/carrito/item/<int:producto_id>')

    # Endpoints del pedido
    api.add_resource(PedidoResource, '/api/pedidos')

    # Endpoints del perfil
    api.add_resource(PerfilResource, '/api/perfil')
    api.add_resource(CambiarContrasenaResource, '/api/usuario/cambiar-contrasena')

    # Endpoints para la lista de deseos
    api.add_resource(DeseoListResource, '/api/deseos')
    api.add_resource(DeseoItemResource, '/api/deseos/<int:producto_id>')
    api.add_resource(DeseoIDsResource, '/api/deseos/ids')

    # Endpoints para el intercambio
    api.add_resource(IntercambioResource, '/api/intercambio')

    # Endpoints para la newsletter
    api.add_resource(NewsletterSubscribeResource, '/api/newsletter/subscribe')

# Si necesitamos un filtro strftime para plantillas Jinja2
# def strftime_filter(value, format='%Y-%m-%d %H:%M'):
#    if value is None:
#        return ""
#    return value.strftime(format)

current_app = create_app()

@current_app.shell_context_processor
def make_shell_context():
    # Esto permite acceder a 'db' y a los modelos desde 'flask shell'
    return dict(
        db=db, Usuario=Usuario, Empresa=Empresa, Categoria=Categoria,
        Juego=Juego, Producto=Producto, CarritoItem=CarritoItem,
        DeseoItem=DeseoItem, InventarioItem=InventarioItem, Pedido=Pedido,
        DetallePedido=DetallePedido, Valoracion=Valoracion
    )

@current_app.route('/')
@current_app.route('/<path:path>')
def serve_react_app(path=None):
    """
    Sirve el index.html principal para la aplicación React.
    React Router se encargará de las sub-rutas en el cliente.
    """
    return render_template("index.html")























