from config.base_datos import bd
from sqlalchemy.dialects import postgresql

class AlmacenModel(bd.Model):
    __tablename__ = 'almacen'
    alm_id = bd.Column(
                                name='alm_id', 
                                type_= bd.Integer, 
                                primary_key=True, 
                                autoincrement=True,
                                nullable=False,
                                unique=True
                            )
    alm_cod = bd.Column(
                                name="alm_cod",
                                type_= postgresql.CHAR(2),
                                nullable=False
                            )
    alm_nom = bd.Column(
                            name="alm_nom",
                            type_= bd.String(50),
                            nullable=False
                        )
    alm_est = bd.Column(
                            name="alm_est",
                            type_= bd.Boolean,
                            default=True
                        )

    almacenes = bd.relationship('ProductoAlmacenModel', backref='almacenProdAlm', lazy=True)

    def __init__(self, codigoAlmacen, nombreAlmacen, estadoAlmacen):
        self.alm_cod = codigoAlmacen
        self.alm_nom = nombreAlmacen
        self.alm_est = estadoAlmacen

    def __str__(self):
        return '{} : {} : {}'.format(self.alm_id, self.alm_cod, self.alm_nom)

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return {
            'almacen_id' : self.alm_id,
            'almacen_codigo' : self.alm_cod,
            'almacen_nombre' : self.alm_nom,
            'almacen_estado' : self.alm_est
        }

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()