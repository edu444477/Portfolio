from extensions import db

class DeseoItem(db.Model):
    __tablename__ = "deseos"

    idDeseo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    numProductos = db.Column(db.Integer, nullable=True, default=1)

    # Relaciones
    usuario = db.relationship("Usuario", backref=db.backref("deseo_items_usuario", lazy="dynamic", cascade="all, delete-orphan"))
    producto = db.relationship("Producto", backref=db.backref("deseado_por_usuarios", lazy="dynamic"))

    # UniqueConstraint está bien
    __table_args__ = (db.UniqueConstraint('idUsuario', 'idProducto', name='uq_usuario_producto_deseo'),)

    def __repr__(self):
        return f"<DeseoItem id={self.idDeseo} usuario_id={self.idUsuario} producto_id={self.idProducto}>"


    def to_dict(self):
        data = {
            'idDeseo': self.idDeseo,
            'idUsuario': self.idUsuario,
            'idProducto': self.idProducto,
        }
        if self.nombre:
            data['nombre_deseo'] = self.nombre
        if self.producto:
            data['producto_info'] = {
                'idProducto': self.producto.idProducto,
                'nombre': self.producto.nombre,
                'foto': self.producto.foto,
                'precio': float(self.producto.precio) if self.producto.precio is not None else None
            }
        return data