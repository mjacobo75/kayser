from flask_restful import Resource, reqparse
from models.producto import ProductoModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'producto_codigo',
    type=str,
    required=True,
    help='Falta producto_codigo',
    location='json'
)
serializer.add_argument(
    'producto_nombre',
    type=str,
    required=True,
    help='Falta producto_nombre',
    location='json'
)
serializer.add_argument(
    'producto_precio',
    type=float,
    required=True,
    help='Falta producto_precio',
    location='json'
)
serializer.add_argument(
    'producto_imagen',
    type=str,
    required=True,
    help='Falta producto_imagen',
    location='json'
)
serializer.add_argument(
    'producto_estado',
    type=bool,
    required=True,
    help='Falta producto_estado',
    location='json'
)
serializer.add_argument(
    'categoriaId',
    type=int,
    required=True,
    help='Falta categoriaId',
    location='json'
)
serializer.add_argument(
    'tipoId',
    type=int,
    required=True,
    help='Falta tipoId',
    location='json'
)

class ProductoController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        nuevoProducto = ProductoModel(informacion['producto_codigo'], informacion['producto_nombre'], informacion['producto_precio'], informacion['producto_imagen'], informacion['producto_estado'], informacion['categoriaId'], informacion['tipoId'])
        nuevoProducto.save()
        productoPresentado = nuevoProducto.json()
        productoPresentado['categoria'] = nuevoProducto.categoriaProducto.json()
        productoPresentado['tipo'] = nuevoProducto.tipoProducto.json()
        return {
            'success' : True,
            'content' : productoPresentado,
            'message' : 'Producto grabado exitosamente..!!'
        }, 201

    def get(self):
        lstProducto = ProductoModel.query.all()
        arregloProducto = []
        for prod in lstProducto:
            resultadoTmp = prod.json()
            resultadoTmp['categoria'] = prod.categoriaProducto.json()
            resultadoTmp['tipo'] = prod.tipoProducto.json() 
            arregloProducto.append(resultadoTmp)

        return {
            'success' : True,
            'content' : arregloProducto,
            'message' : None
        }, 201

class ProductoUnicoController(Resource):
    def get(self, idProducto):
        productoEncontrado = ProductoModel.query.filter_by(prod_id=idProducto).first()
        productoPresentado = productoEncontrado.json()
        productoPresentado['categoria'] = productoEncontrado.categoriaProducto.json()
        productoPresentado['tipo'] = productoEncontrado.tipoProducto.json()
        
        if productoEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Producto no encontrado..!'
            }, 404
        else:
            return{
                'success' : True,
                'content' : productoPresentado,
                'message' : 'Registro econtrado..!'
            }

    def put(self, idProducto):
        productoEncontrado = ProductoModel.query.filter_by(prod_id=idProducto).first()
        if productoEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Producto no encontrado..!'
            }, 404
        else:
            informacion = serializer.parse_args()
            productoEncontrado.prod_cod = informacion['producto_codigo']
            productoEncontrado.prod_nom = informacion['producto_nombre']
            productoEncontrado.prod_pre = informacion['producto_precio']
            productoEncontrado.prod_img = informacion['producto_imagen']
            productoEncontrado.prod_est = informacion['producto_estado']
            productoEncontrado.categoria = informacion['categoriaId']
            productoEncontrado.prodTipo = informacion['tipoId']
            productoEncontrado.save()
            productoPresentado = productoEncontrado.json()
            productoPresentado['categoria'] = productoEncontrado.categoriaProducto.json()
            productoPresentado['tipo'] = productoEncontrado.tipoProducto.json()
            return{
                'success' : True,
                'content' : productoPresentado,
                'message' : 'Registro modificado existosamente..!'
            }

    def delete(self, idProducto):
        productoEncontrado = ProductoModel.query.filter_by(prod_id=idProducto).first()
        if productoEncontrado:
            productoEncontrado.delete()
            return{
                'success' : True,
                'content' : None,
                'message' : 'Se eliminó existosamente el producto de la BD..!'
            }
        else:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Producto no encontrado..!'
            }, 404