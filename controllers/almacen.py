from flask_restful import Resource, reqparse
from models.almacen import AlmacenModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'almacen_codigo',
    type=str,
    required=True,
    help='Falta almacen_codigo',
    location='json'
)
serializer.add_argument(
    'almacen_nombre',
    type=str,
    required=True,
    help='Falta almacen_nombre',
    location='json'
)
serializer.add_argument(
    'almacen_estado',
    type=bool,
    required=True,
    help='Falta almacen_estado',
    location='json'
)

class AlmacenController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        nuevoAlmacen = AlmacenModel(informacion['almacen_codigo'], informacion['almacen_nombre'], informacion['almacen_estado'])
        nuevoAlmacen.save()
        return {
            'success' : True,
            'content' : nuevoAlmacen.json(),
            'message' : 'Categoria grabada exitosamente..!!'
        }, 201

    def get(self):
        lstAlmacen = AlmacenModel.query.all()
        arregloAlmacen = []
        for alm in lstAlmacen:
            arregloAlmacen.append(alm.json())

        return {
            'success' : True,
            'content' : arregloAlmacen,
            'message' : None
        }, 201

class AlmacenUnicoController(Resource):
    def get(self, idAlmacen):
        almacenEncontrado = AlmacenModel.query.filter_by(alm_id=idAlmacen).first()
        if almacenEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Almacén no encontrado..!'
            }, 404
        else:
            return{
                'success' : True,
                'content' : almacenEncontrado.json(),
                'message' : 'Registro econtrado..!'
            }

    def put(self, idAlmacen):
        almacenEncontrado = AlmacenModel.query.filter_by(alm_id=idAlmacen).first()
        if almacenEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Almacén no encontrado..!'
            }, 404
        else:
            informacion = serializer.parse_args()
            almacenEncontrado.alm_cod = informacion['almacen_codigo']
            almacenEncontrado.alm_nom = informacion['almacen_nombre']
            almacenEncontrado.alm_est = informacion['almacen_estado']
            almacenEncontrado.save()
            return{
                'success' : True,
                'content' : almacenEncontrado.json(),
                'message' : 'Registro modificado existosamente..!'
            }

    def delete(self, idAlmacen):
        almacenEncontrado = AlmacenModel.query.filter_by(alm_id=idAlmacen).first()
        if almacenEncontrado:
            almacenEncontrado.delete()
            return{
                'success' : True,
                'content' : None,
                'message' : 'Se eliminó existosamente la categoría de la BD..!'
            }
        else:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Almacén no encontrado..!'
            }, 404

# busqueda de todos los productos que tiene un almacen
class AlmacenProductoController(Resource):
    def get(self, idAlmacen):
        almacenEncontrado = AlmacenModel.query.filter_by(alm_id=idAlmacen).first()
        productosAlmacen = almacenEncontrado.almacenes
        prods = []
        for prod in productosAlmacen:
            producto = prod.productoProdAlm.json()
            # agregando el objeto categoría del producto
            producto['categoria'] = prod.productoProdAlm.categoriaProducto.json()
            # agregando el campo "nombre" del objeto tipo-producto
            producto['tipo'] = prod.productoProdAlm.tipoProducto.prodtipo_nom
            prods.append(producto)

        resultado = almacenEncontrado.json()
        resultado['productos'] = prods

        return {
            'success' : True,
            'content' : resultado,
            'message' : 'consulta exitosa..!'
        }

#Consulta de productos que contemplen un almacen y una categoria 
class CategoriaAlmacenProductoController(Resource):
    def get(self):
        serializer.remove_argument('almacen_codigo')
        serializer.remove_argument('almacen_nombre')
        serializer.remove_argument('almacen_estado')
        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta categoria',
            location='args'
        )
        serializer.add_argument(
            'almacen',
            type=int,
            required=True,
            help='Falta almacen',
            location='args'
        )
        informacion = serializer.parse_args()
        alm = AlmacenModel.query.filter_by(alm_id=informacion['almacen']).first()
        productos = []
        for producto in alm.almacenes:
            if (producto.productoProdAlm.categoria == informacion['categoria']):
                presentacion = producto.productoProdAlm.json()
                presentacion['stock'] = producto.prodAlm_stk
                productos.append(presentacion)

        return {
            'success' : True,
            'content' : productos,
            'message' : 'consulta satisfactoria..!!'
        }
        