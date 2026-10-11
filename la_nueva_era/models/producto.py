from extensions import db

class Producto(db.Model):
    __tablename__ = "productos"

    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'), nullable=False)
    idJuego = db.Column(db.Integer, db.ForeignKey('juegos.idJuego'), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    calidad = db.Column(db.String(30), nullable=False)
    precio = db.Column(db.Numeric(7, 2), nullable=False)
    foto = db.Column(db.String(30), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)

    # Relaciones
    categoria = db.relationship("Categoria", back_populates="productos")
    juego = db.relationship("Juego", back_populates="productos")
    valoraciones = db.relationship("Valoracion", back_populates="producto")

    def __repr__(self):
        return f"<Producto(nombre='{self.nombre}')>"

    def to_dict(self):
        return {
            'idProducto': self.idProducto,
            'idCategoria': self.idCategoria,
            'idJuego': self.idJuego,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'calidad': self.calidad,
            'precio': float(self.precio) if self.precio is not None else None,
            'foto': self.foto,
            'categoria_nombre': self.categoria.nombre if self.categoria else None,
            'juego_nombre': self.juego.nombre if self.juego else None,
            'stock': self.stock
        }