from config.base_datos import bd
from sqlalchemy.dialects import postgresql

class ProductoModel(bd.Model):
    __tablename__ = 'producto'
    prod_id = bd.Column(
                            name='prod_id', 
                            type_= bd.Integer, 
                            primary_key=True, 
                            autoincrement=True,
                            nullable=False,
                            unique=True
                        )
    prod_cod = bd.Column(
                            name="prod_cod",
                            type_= postgresql.CHAR(6),
                            nullable=False
                        )
    prod_nom = bd.Column(
                            name="prod_nom",
                            type_= bd.String(70),
                            nullable=False
                        )
    prod_pre = bd.Column(
                            name="prod_pre",
                            type_= bd.Float(),
                            default=0
                        )
    prod_img = bd.Column(
                            name="prod_img",
                            type_= bd.String(100)
                        )
    prod_est = bd.Column(
                            name="prod_est",
                            type_= bd.Boolean,
                            default=True
                        )
    
    #Relaciones (FK)
    categoria = bd.Column(bd.ForeignKey('categoria.cat_id'), name='cat_id', type_= bd.Integer, nullable=False, default=0)
    prodTipo = bd.Column(bd.ForeignKey('producto_tipo.prodt_id'), name='prodt_id', type_= bd.Integer, nullable=False, default=0)

    productos = bd.relationship('ProductoAlmacenModel', backref='productoProdAlm', lazy=True)

    def __init__(self, codigoProducto, nombreProducto, precio, imagen, estado, categoriaId, tipoId):
        self.prod_cod = codigoProducto
        self.prod_nom = nombreProducto
        self.prod_pre = precio
        self.prod_img = imagen
        self.prod_est = estado
        self.categoria = categoriaId
        self.prodTipo = tipoId

    def __str__(self):
        return '{} : {}'.format(self.prod_id, self.prod_nom)

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'producto_id' : self.prod_id,
            'producto_codigo' : self.prod_cod,
            'producto_nombre' : self.prod_nom,
            'producto_precio' : self.prod_pre,
            'producto_imagen' : self.prod_img,
            'producto_estado' : self.prod_est
        }

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()