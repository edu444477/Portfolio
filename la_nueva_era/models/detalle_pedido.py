from extensions import db

class DetallePedido(db.Model):
    __tablename__ = "detallepedidos"

    idPedido = db.Column(db.Integer, db.ForeignKey('pedidos.idPedido'), primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'), primary_key=True)
    numProductos = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(7, 2), nullable=False)

    # Relaciones
    pedido = db.relationship("Pedido", back_populates="detalles")
    producto = db.relationship("Producto", backref=db.backref("en_detalle_pedidos", lazy="dynamic"))


    def __repr__(self):
        return f"<DetallePedido(pedido_id={self.idPedido}, producto_id={self.idProducto}, cantidad={self.numProductos})>"

    def to_dict(self):
        return {
            'idPedido': self.idPedido,
            'idProducto': self.idProducto,
            'numProductos': self.numProductos,
            'valor': float(self.valor) if self.valor is not None else None,
            'producto_nombre': self.producto.nombre if self.producto else None
        }