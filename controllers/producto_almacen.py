from flask_restful import Resource, reqparse
from models.producto_almacen import ProductoAlmacenModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'prod_alm_stk',
    type=int,
    required=True,
    help='Falta Stock',
    location='json'
)
serializer.add_argument(
    'prod_alm_est',
    type=bool,
    required=True,
    help='Falta Estado',
    location='json'
)
serializer.add_argument(
    'producto_id',
    type=int,
    required=True,
    help='Falta Producto Id',
    location='json'
)
serializer.add_argument(
    'almacen_id',
    type=int,
    required=True,
    help='Falta Almacén Id',
    location='json'
)

class ProductoAlmacenController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        nuevoProdAlm = ProductoAlmacenModel(informacion['producto_id'], informacion['almacen_id'], informacion['prod_alm_stk'], informacion['prod_alm_est'])
        nuevoProdAlm.save()
        return {
            'success' : True,
            'content' : nuevoProdAlm.json(),
            'message' : 'Producto-Almacén grabado exitosamente..!!'
        }, 201

    def get(self):
        lstProdAlm = ProductoAlmacenModel.query.all()
        arregloProdAlm = []
        for prodAlm in lstProdAlm:
            arregloProdAlm.append(prodAlm.json())

        return {
            'success' : True,
            'content' : arregloProdAlm,
            'message' : None
        }, 201