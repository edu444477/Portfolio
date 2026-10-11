from extensions import db

class Valoracion(db.Model):
    __tablename__ = "valoraciones"

    idValoracion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)

    # Relaciones
    usuario = db.relationship("Usuario", back_populates="valoraciones")
    producto = db.relationship("Producto", back_populates="valoraciones")

    def __repr__(self):
        return f"<Valoracion(usuario_id={self.idUsuario}, producto_id={self.idProducto}, nota={self.nota})>"

    def to_dict(self):
        return {
            'idValoracion': self.idValoracion,
            'idUsuario': self.idUsuario,
            'idProducto': self.idProducto,
            'nota': self.nota,
            'comentario': self.comentario,
            'usuario_nombre': self.usuario.usuario if self.usuario else None,
            'producto_nombre': self.producto.nombre if self.producto else None
        }