from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Usuario
from datetime import datetime, date
import decimal

# Parser para actualizar datos del perfil
update_perfil_parser = reqparse.RequestParser(bundle_errors=True)
update_perfil_parser.add_argument('nombre', type=str, required=False, store_missing=False, help='Nombre del usuario')
update_perfil_parser.add_argument('apellidos', type=str, required=False, store_missing=False, help='Apellidos del usuario (puede ser vacío)')
update_perfil_parser.add_argument('fecha_nacimiento', type=str, required=False, store_missing=False, help='Fecha de nacimiento (YYYY-MM-DD)')
update_perfil_parser.add_argument('foto', type=str, required=False, store_missing=False, help='Ruta/nombre del avatar seleccionado')
update_perfil_parser.add_argument('saldo', type=str, required=False, store_missing=False, help='Nuevo saldo')

# Parser para cambiar contraseña
change_password_parser = reqparse.RequestParser(bundle_errors=True)
change_password_parser.add_argument('contrasena_actual', type=str, required=True, help='La contraseña actual es obligatoria.')
change_password_parser.add_argument('nueva_contrasena', type=str, required=True, help='La nueva contraseña es obligatoria.')
change_password_parser.add_argument('confirmar_nueva_contrasena', type=str, required=True, help='La confirmación de la nueva contraseña es obligatoria.')


class PerfilResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(int(user_id))

        if not usuario:
            return {'message': 'Usuario no encontrado'}, 404

        return usuario.to_dict(), 200
        # Alternativa manual si to_dict no es suficiente:
        # return {
        #     'idUsuario': usuario.idUsuario,
        #     'nombre_usuario': usuario.usuario,
        #     'email': usuario.correo,
        #     'nombre': usuario.nombre,
        #     'apellidos': usuario.apellidos,
        #     'fecha_nacimiento': usuario.fech_nac.isoformat() if isinstance(usuario.fech_nac, date) else None,
        #     'foto': usuario.foto,
        #     'saldo': float(usuario.saldo) if usuario.saldo is not None else 0.0
        # }, 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(int(user_id))

        if not usuario:
            return {'message': 'Usuario no encontrado'}, 404

        args = update_perfil_parser.parse_args()

        # Verificar si se envió al menos un campo para actualizar
        if not args: # Si args está vacío porque no se envió ningún campo editable
            return {'message': 'No se proporcionaron datos para actualizar.'}, 400

        updated_fields_count = 0

        if 'nombre' in args:
            if not args['nombre'].strip():
                 return {'message': 'El nombre no puede estar vacío.'}, 400
            usuario.nombre = args['nombre']
            updated_fields_count +=1

        if 'apellidos' in args:
            usuario.apellidos = args['apellidos']
            updated_fields_count +=1

        if 'fecha_nacimiento' in args:
            try:
                fecha_nac_obj = datetime.strptime(args['fecha_nacimiento'], '%Y-%m-%d').date()
                hoy = date.today()
                edad = hoy.year - fecha_nac_obj.year - ((hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day))
                if edad < 18:
                    return {'message': 'Debes tener al menos 18 años.'}, 400
                usuario.fech_nac = fecha_nac_obj
                updated_fields_count +=1
            except ValueError:
                return {'message': 'Formato de fecha de nacimiento inválido. Use YYYY-MM-DD.'}, 400

        if 'foto' in args:
            usuario.foto = args['foto']
            updated_fields_count +=1

        if 'saldo' in args:
            try:
                nuevo_saldo = decimal.Decimal(args['saldo'])
                if nuevo_saldo < decimal.Decimal('0.00'):
                    return {'message': 'El saldo no puede ser negativo.'}, 400
                if nuevo_saldo > decimal.Decimal('99999.99'):
                    return {'message': 'El saldo excede el límite máximo permitido (99999.99).'}, 400

                usuario.saldo = nuevo_saldo
                updated_fields_count +=1
            except decimal.InvalidOperation:
                return {'message': 'Formato de saldo inválido. Use un número como "123.45".'}, 400
            except ValueError:
                return {'message': 'Valor de saldo inválido.'}, 400

        if updated_fields_count == 0:
             return {'message': 'No se proporcionaron datos válidos para actualizar.'}, 400

        try:
            db.session.commit()
            return {'message': 'Perfil actualizado correctamente.', 'perfil': usuario.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar perfil para usuario {user_id}: {e}")
            return {'message': 'Error interno al actualizar el perfil.'}, 500


class CambiarContrasenaResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(int(user_id))

        if not usuario:
            return {'message': 'Usuario no encontrado'}, 404

        args = change_password_parser.parse_args()

        if not usuario.check_password(args['contrasena_actual']):
            return {'message': 'La contraseña actual es incorrecta.'}, 400

        if args['nueva_contrasena'] != args['confirmar_nueva_contrasena']:
            return {'message': 'La nueva contraseña y la confirmación no coinciden.'}, 400

        nueva_clave = args['nueva_contrasena']
        errors = {}
        if len(nueva_clave) < 6:
            errors['nueva_contrasena_longitud'] = 'La nueva contraseña debe tener al menos 6 caracteres.'
        if not any(char.isupper() for char in nueva_clave):
            errors['nueva_contrasena_mayuscula'] = 'La nueva contraseña debe contener al menos una mayúscula.'

        if errors:
            return {'message': 'Errores de validación en la nueva contraseña.', 'errors': errors}, 400


        usuario.set_password(nueva_clave)

        try:
            db.session.commit()
            return {'message': 'Contraseña actualizada correctamente.'}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error al cambiar contraseña para usuario {user_id}: {e}")
            return {'message': 'Error interno al cambiar la contraseña.'}, 500