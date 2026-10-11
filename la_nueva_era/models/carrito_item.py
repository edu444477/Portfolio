from extensions import db

class CarritoItem(db.Model):
    __tablename__ = "carritos"

    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'), primary_key=True)
    numProductos = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(7, 2), nullable=False)

    # Relaciones para acceder al usuario y al producto desde un item del carrito
    usuario = db.relationship("Usuario", backref=db.backref("carrito_items", lazy="dynamic"))
    producto = db.relationship("Producto", backref=db.backref("en_carritos", lazy="dynamic"))

    def __repr__(self):
        return f"<CarritoItem(usuario_id={self.idUsuario}, producto_id={self.idProducto}, cantidad={self.numProductos})>"

    def to_dict(self):
        return {
            'idUsuario': self.idUsuario,
            'idProducto': self.idProducto,
            'numProductos': self.numProductos,
            'valor': float(self.valor) if self.valor is not None else None,
            'producto_nombre': self.producto.nombre if self.producto else None # Ejemplo
        }