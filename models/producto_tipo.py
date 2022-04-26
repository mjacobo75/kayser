from config.base_datos import bd
from sqlalchemy.orm import relationship

class ProductoTipoModel(bd.Model):
    __tablename__ = 'producto_tipo'
    prodtipo_id = bd.Column(
                                name='prodt_id', 
                                type_= bd.Integer, 
                                primary_key=True, 
                                autoincrement=True,
                                nullable=False,
                                unique=True
                            )
    prodtipo_nom = bd.Column(
                                name="prodt_nom",
                                type_= bd.String(30),
                                nullable=False
                            )
    
    productos = bd.relationship('ProductoModel', backref='tipoProducto', lazy=True)

    def __init__(self, nombreTipo):
        self.prodtipo_nom = nombreTipo

    def __str__(self):
        return '{} : {}'.format(self.prodtipo_id, self.prodtipo_nom)

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'tipo_id' : self.prodtipo_id,
            'tipo_nombre' : self.prodtipo_nom
        }

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()