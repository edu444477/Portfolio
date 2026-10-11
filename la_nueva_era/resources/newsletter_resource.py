from flask_restful import Resource, reqparse
from models import db
from models.newsletter import Newsletter as NewsletterModel
from sqlalchemy.exc import IntegrityError
import re

subscribe_parser = reqparse.RequestParser()
subscribe_parser.add_argument('correo', type=str, required=True, help="El correo electrónico es obligatorio.", location='json')

def is_valid_email(email):
    if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        return True
    return False

class NewsletterSubscribeResource(Resource):
    def post(self):
        args = subscribe_parser.parse_args()
        correo = args['correo'].strip()

        if not correo:
            return {'message': 'El correo electrónico no puede estar vacío.'}, 400
        
        if not is_valid_email(correo):
            return {'message': 'El formato del correo electrónico no es válido.'}, 400

        existente = NewsletterModel.query.filter_by(correo=correo).first()
        if existente:
            return {'message': 'Este correo electrónico ya está suscrito a nuestro newsletter.'}, 200

        nueva_suscripcion = NewsletterModel(correo=correo)
        db.session.add(nueva_suscripcion)

        try:
            db.session.commit()
            return {'message': '¡Gracias por suscribirte a nuestro newsletter!'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Este correo electrónico ya está suscrito.'}, 409 # Conflict
        except Exception as e:
            db.session.rollback()
            print(f"Error al suscribir al newsletter: {e}")
            return {'message': 'Error interno al procesar la suscripción.'}, 500