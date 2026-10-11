from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from sqlalchemy import or_
from datetime import datetime

from models import db
from models import Usuario

# Parser para el registro
register_parser = reqparse.RequestParser()
register_parser.add_argument('nombre', type=str, required=True, help='El nombre es obligatorio')
register_parser.add_argument('apellidos', type=str, required=False)
register_parser.add_argument('usuario', type=str, required=True, help='El nombre de usuario es obligatorio')
register_parser.add_argument('clave', type=str, required=True, help='La clave es obligatoria')
register_parser.add_argument('correo', type=str, required=True, help='El correo electrónico es obligatorio')
register_parser.add_argument('fech_nac', type=str, required=True, help='La fecha de nacimiento es obligatoria (YYYY-MM-DD)')

# Parser para el login
login_parser = reqparse.RequestParser()
login_parser.add_argument('identificador', type=str, required=True, help='El usuario o correo es obligatorio') # Acepta usuario o correo
login_parser.add_argument('clave', type=str, required=True, help='La clave es obligatoria')

# --- Resources ---

class RegisterResource(Resource):
    def post(self):
        args = register_parser.parse_args()

        # Verificar si el usuario o correo ya existen
        if Usuario.query.filter(or_(Usuario.usuario == args['usuario'], Usuario.correo == args['correo'])).first():
            return {'message': 'El nombre de usuario o correo electrónico ya existe'}, 409 # 409 Conflict

        # Validar formato de fecha
        try:
            fecha_nac_obj = datetime.strptime(args['fech_nac'], '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Formato de fecha inválido. Use YYYY-MM-DD'}, 400

        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=args['nombre'],
            apellidos=args['apellidos'] if args['apellidos'] else '',
            usuario=args['usuario'],
            correo=args['correo'],
            fech_nac=fecha_nac_obj,
        )
        # Hashear la contraseña ANTES de guardar
        nuevo_usuario.set_password(args['clave'])

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar usuario: {e}")
            return {'message': 'Error interno al registrar el usuario'}, 500

        # Devolver solo ID y un mensaje (o el dict completo)
        return {'message': 'Usuario registrado exitosamente', 'usuario_id': nuevo_usuario.idUsuario}, 201


class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        identificador = args['identificador']
        clave = args['clave']

        user = Usuario.query.filter(or_(Usuario.usuario == identificador, Usuario.correo == identificador)).first()

        if user and user.check_password(clave):
            access_token = create_access_token(identity=str(user.idUsuario))

            # Crear el objeto de usuario para enviar al frontend
            user_data_for_frontend = {
                'idUsuario': user.idUsuario,
                'usuario': user.usuario,
                'nombre': user.nombre,
                'apellidos': user.apellidos,
                'correo': user.correo,
                'fech_nac': user.fech_nac.isoformat() if user.fech_nac else None,
                'foto': user.foto,
                'saldo': float(user.saldo) if user.saldo is not None else 0.00
            }

            return {
                'access_token': access_token,
                'user': user_data_for_frontend
            }, 200
        else:
            return {'message': 'Credenciales inválidas'}, 401












