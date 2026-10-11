from extensions import db, bcrypt
from datetime import date

class Usuario(db.Model):
    __tablename__ = "usuarios"

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(120), nullable=True, default="")
    usuario = db.Column(db.String(30), nullable=False, unique=True)
    clave_hash = db.Column(db.String(128), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True)
    fech_nac = db.Column(db.Date, nullable=False)
    saldo = db.Column(db.Numeric(7, 2), nullable=False, default=0.00)
    foto = db.Column(db.String(120), nullable=True)

    # Relaciones
    pedidos = db.relationship("Pedido", back_populates="usuario")
    valoraciones = db.relationship("Valoracion", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(usuario='{self.usuario}')>"

    def set_password(self, password):
        self.clave_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.clave_hash, password)

    def to_dict(self):
        return {
            'idUsuario': self.idUsuario,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'usuario': self.usuario,
            'correo': self.correo,
            'fech_nac': self.fech_nac.isoformat() if isinstance(self.fech_nac, date) else self.fech_nac,
            'saldo': float(self.saldo) if self.saldo is not None else None,
            'foto': self.foto
        }