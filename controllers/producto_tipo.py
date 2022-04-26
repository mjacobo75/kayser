from flask_restful import Resource, reqparse
from models.producto_tipo import ProductoTipoModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'tipo_nombre',
    type=str,
    required=True,
    help='Falta tipo_nombre',
    location='json'
)

class TipoProductoController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        nuevoTipo = ProductoTipoModel(informacion['tipo_nombre'])
        nuevoTipo.save()
        print(nuevoTipo)
        return {
            'success' : True,
            'content' : nuevoTipo.json(),
            'message' : 'Tipo de Producto grabado exitosamente..!!'
        }, 201

    def get(self):
        lstTipo = ProductoTipoModel.query.all()
        arregloTipo = []
        for tipo in lstTipo:
            arregloTipo.append(tipo.json())

        return {
            'success' : True,
            'content' : arregloTipo,
            'message' : None
        }, 201

class TipoProductoUnicoController(Resource):
    def get(self, idTipo):
        tipoEncontrado = ProductoTipoModel.query.filter_by(prodtipo_id=idTipo).first()
        if tipoEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Tipo de Producto no encontrado..!'
            }, 404
        else:
            return{
                'success' : True,
                'content' : tipoEncontrado.json(),
                'message' : 'Registro econtrado..!'
            }

    def put(self, idTipo):
        tipoEncontrado = ProductoTipoModel.query.filter_by(prodtipo_id=idTipo).first()
        if tipoEncontrado is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Tipo de Producto no encontrado..!'
            }, 404
        else:
            informacion = serializer.parse_args()
            tipoEncontrado.prodtipo_nom = informacion['tipo_nombre']
            tipoEncontrado.save()
            return{
                'success' : True,
                'content' : tipoEncontrado.json(),
                'message' : 'Registro modificado existosamente..!'
            }

    def delete(self, idTipo):
        tipoEncontrado = ProductoTipoModel.query.filter_by(prodtipo_id=idTipo).first()
        if tipoEncontrado:
            tipoEncontrado.delete()
            return{
                'success' : True,
                'content' : None,
                'message' : 'Se eliminó existosamente el Tipo de Producto de la BD..!'
            }
        else:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Tipo de Producto no encontrado..!'
            }, 404