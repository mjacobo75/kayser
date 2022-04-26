from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel

serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'categoria_nombre',
    type=str,
    required=True,
    help='Falta categoria_nombre',
    location='json'
)
serializer.add_argument(
    'categoria_estado',
    type=bool,
    required=True,
    help='Falta categoria_estado',
    location='json'
)

class CategoriaController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        nuevaCategoria = CategoriaModel(informacion['categoria_nombre'], informacion['categoria_estado'])
        nuevaCategoria.save()
        return {
            'success' : True,
            'content' : nuevaCategoria.json(),
            'message' : 'Categoria grabada exitosamente..!!'
        }, 201

    def get(self):
        lstCategoria = CategoriaModel.query.all()
        arregloCategoria = []
        for cat in lstCategoria:
            arregloCategoria.append(cat.json())

        return {
            'success' : True,
            'content' : arregloCategoria,
            'message' : None
        }, 201

class CategoriaUnicaController(Resource):
    def get(self, idCategoria):
        categoriaEncontrada = CategoriaModel.query.filter_by(cat_id=idCategoria).first()
        if categoriaEncontrada is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Categoría no encontrada..!'
            }, 404
        else:
            return{
                'success' : True,
                'content' : categoriaEncontrada.json(),
                'message' : 'Registro econtrado..!'
            }

    def put(self, idCategoria):
        categoriaEncontrada = CategoriaModel.query.filter_by(cat_id=idCategoria).first()
        if categoriaEncontrada is None:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Categoría no encontrada..!'
            }, 404
        else:
            informacion = serializer.parse_args()
            categoriaEncontrada.cat_nom = informacion['categoria_nombre']
            categoriaEncontrada.cat_est = informacion['categoria_estado']
            categoriaEncontrada.save()
            return{
                'success' : True,
                'content' : categoriaEncontrada.json(),
                'message' : 'Registro modificado existosamente..!'
            }

    def delete(self, idCategoria):
        categoriaEncontrada = CategoriaModel.query.filter_by(cat_id=idCategoria).first()
        if categoriaEncontrada:
            categoriaEncontrada.delete()
            return{
                'success' : True,
                'content' : None,
                'message' : 'Se eliminó existosamente la categoría de la BD..!'
            }
        else:
            return{
                'success' : False,
                'content' : None,
                'message' : 'Categoría no encontrada..!'
            }, 404