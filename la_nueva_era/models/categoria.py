from extensions import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    idCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(30), nullable=True)

    # Relaciones
    productos = db.relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(nombre='{self.nombre}')>"

    def to_dict(self):
        return {
            'idCategoria': self.idCategoria,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'foto': self.foto
        }