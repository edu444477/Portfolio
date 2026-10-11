from extensions import db
from datetime import date

class Pedido(db.Model):
    __tablename__ = "pedidos"

    idPedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    total = db.Column(db.Numeric(7, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    estado = db.Column(db.String(50), nullable=False, default="Pendiente")

    # Relaciones
    usuario = db.relationship("Usuario", back_populates="pedidos")
    detalles = db.relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido(id={self.idPedido}, usuario_id={self.idUsuario}, estado='{self.estado}')>"

    def to_dict(self):
        return {
            'idPedido': self.idPedido,
            'idUsuario': self.idUsuario,
            'total': float(self.total) if self.total is not None else None,
            'fecha': self.fecha.isoformat() if isinstance(self.fecha, date) else self.fecha,
            'estado': self.estado,
            'usuario_nombre': self.usuario.usuario if self.usuario else None,
            'detalles': [detalle.to_dict() for detalle in self.detalles] if self.detalles else []
        }