from config.base_datos import bd
from sqlalchemy.orm import relationship

class ProductoAlmacenModel(bd.Model):
    __tablename__ = 'producto_almacen'
    prodAlm_id = bd.Column(
                                name='prodAlm_id', 
                                type_= bd.Integer, 
                                primary_key=True, 
                                autoincrement=True,
                                nullable=False,
                                unique=True
                            )
    prodAlm_stk = bd.Column(
                                name='prodAlm_stk', 
                                type_= bd.Integer,
                                nullable=False
                            )
    prodAlm_est = bd.Column(
                                name='prodAlm_est', 
                                type_= bd.Boolean,
                                nullable=False,
                                default='true'
                            )
    #Relaciones (FK)
    producto = bd.Column(bd.ForeignKey('producto.prod_id'), name='prod_id', type_= bd.Integer, nullable=False)
    almacen = bd.Column(bd.ForeignKey('almacen.alm_id'), name='alm_id', type_= bd.Integer, nullable=False)

    def __init__(self, idProducto, idAlmacen, stock, estado):
        self.producto = idProducto
        self.almacen = idAlmacen
        self.prodAlm_stk = stock
        self.prodAlm_est = estado

    def save(self):
        bd.session.add(self)
        bd.session.commit()
    
    def json(self):
        return {
            'prod_alm_id' : self.prodAlm_id,
            'prod_alm_stk' : self.prodAlm_stk,
            'prod_alm_est' : self.prodAlm_est,
            'producto_id' : self.producto,
            'almacen_id' : self.almacen
        }
    
    def delete(self):
        bd.session.delete(self)
        bd.session.commit()