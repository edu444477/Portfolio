from extensions import db

class Juego(db.Model):
    __tablename__ = "juegos"

    idJuego = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idEmpresa = db.Column(db.Integer, db.ForeignKey('empresas.idEmpresa'), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    plataforma = db.Column(db.String(30), nullable=False)
    web = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.String(30), nullable=True)

    # Relaciones
    empresa = db.relationship("Empresa", back_populates="juegos")
    productos = db.relationship("Producto", back_populates="juego")

    def __repr__(self):
        return f"<Juego(nombre='{self.nombre}')>"

    def to_dict(self):
        return {
            'idJuego': self.idJuego,
            'idEmpresa': self.idEmpresa,
            'nombre': self.nombre,
            'plataforma': self.plataforma,
            'web': self.web,
            'foto': self.foto,
            'empresa_nombre': self.empresa.nombre if self.empresa else None
        }