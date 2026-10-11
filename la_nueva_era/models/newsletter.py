from extensions import db

class Newsletter(db.Model):
    __tablename__ = 'newsletter'
    idNewsletter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correo = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f"<Newsletter(correo='{self.correo}')>"

    def to_dict(self):
        return {
            'idNewsletter': self.idNewsletter,
            'correo': self.correo
        }