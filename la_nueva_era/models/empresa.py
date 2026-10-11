from extensions import db

class Empresa(db.Model):
    __tablename__ = "empresas"

    idEmpresa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    web = db.Column(db.String(120), nullable=False)

    # Relaciones
    juegos = db.relationship("Juego", back_populates="empresa")

    def __repr__(self):
        return f"<Empresa(nombre='{self.nombre}')>"

    def to_dict(self):
        return {
            'idEmpresa': self.idEmpresa,
            'nombre': self.nombre,
            'web': self.web
        }