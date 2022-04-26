from config.base_datos import bd

class CategoriaModel(bd.Model):
    __tablename__ = 'categoria'
    cat_id = bd.Column(
                                name='cat_id', 
                                type_= bd.Integer, 
                                primary_key=True, 
                                autoincrement=True,
                                nullable=False,
                                unique=True
                            )
    cat_nom = bd.Column(
                                name="cat_nom",
                                type_= bd.String(15),
                                nullable=False
                            )
    cat_est = bd.Column(
                                name="cat_est",
                                type_= bd.Boolean,
                                default=True
                            )
    productos = bd.relationship('ProductoModel', backref='categoriaProducto', lazy=True)
    
    def __init__(self, nombreCategoria, estadoCategoria):
        self.cat_nom = nombreCategoria
        self.cat_est = estadoCategoria

    def __str__(self):
        return '{} : {} : {}'.format(self.cat_id, self.cat_nom, self.cat_est)

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'categoria_id' : self.cat_id,
            'categoria_nombre' : self.cat_nom,
            'categoria_estado' : self.cat_est
        }

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()