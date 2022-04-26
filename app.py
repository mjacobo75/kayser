from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
from controllers.categoria import CategoriaController, CategoriaUnicaController
from controllers.producto_tipo import TipoProductoController, TipoProductoUnicoController
from controllers.producto import ProductoController, ProductoUnicoController
from controllers.almacen import AlmacenController, AlmacenUnicoController, AlmacenProductoController, CategoriaAlmacenProductoController
from controllers.producto_almacen import ProductoAlmacenController
from models.producto import ProductoModel
from flask_cors import CORS
# Para la documentación
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app-name' : 'Libreria Flask - Swagger Documentation'
    }
)

app = Flask(__name__)
app.register_blueprint(swaggerui_blueprint)

api = Api(app)
CORS(app) #permitiendo todos los metodos, dominios y headers.

# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4580219@localhost:5432/kayser'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#iniciando la aplicacion
bd.init_app(app)
#bd.drop_all(app=app)
#conectando la aplicacion con la base_datos
#previamente debemos tener instalado el driver para la base_datos a conectarse
#para postgresql es : pip install postgres o pip install psycopg2

bd.create_all(app=app)

@app.route('/buscar')
def buscarProducto():
    palabraBuscar = request.args.get('nombre')
    if palabraBuscar:
        buscar = ProductoModel.query.filter(ProductoModel.prod_nom.like('%' + palabraBuscar + '%')).all()
        if buscar:
            resultado = []
            for producto in buscar:
                resultado.append(producto.json())
            return {
                'success' : True,
                'content' : resultado,
                'message' : None
            }
    return {
                'success' : False,
                'content' : None,
                'message' : 'no se encontraron coincidencias con esa palabra'
    }

api.add_resource(CategoriaController, '/categoria')
api.add_resource(CategoriaUnicaController, '/categoria/<int:idCategoria>')
api.add_resource(TipoProductoController, '/tipo')
api.add_resource(TipoProductoUnicoController, '/tipo/<int:idTipo>')
api.add_resource(ProductoController, '/producto')
api.add_resource(ProductoUnicoController, '/producto/<int:idProducto>')
api.add_resource(AlmacenController, '/almacen')
api.add_resource(AlmacenUnicoController, '/almacen/<int:idAlmacen>')
api.add_resource(ProductoAlmacenController, '/prodalm')
api.add_resource(AlmacenProductoController, '/prodalm/<int:idAlmacen>')
api.add_resource(CategoriaAlmacenProductoController,'/bucarproducto')

if __name__ == '__main__':
    app.run(debug=True, port=5000)