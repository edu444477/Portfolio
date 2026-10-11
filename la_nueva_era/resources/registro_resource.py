from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.registro import Registro
from extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

class RegistroResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()  # Obtiene la identidad del usuario del token
            id_trabajador = int(current_user_id) # Convierte a int

            hora_entrada_str = request.get_json().get('hora_entrada')

            if not hora_entrada_str:
                return {'message': 'Hora de entrada es requerida'}, HTTPStatus.BAD_REQUEST

            try:
                hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M:%S').time()  # Convierte el string a time
            except ValueError:
                return {'message': 'Formato de hora de entrada inválido. Use HH:MM:SS'}, HTTPStatus.BAD_REQUEST

            # Crea un objeto datetime para la hora de entrada (combina con la fecha actual)
            now = datetime.utcnow()
            fecha_actual = now.date()
            hora_entrada_completa = datetime.combine(fecha_actual, hora_entrada)

            # Crea el nuevo registro
            nuevo_registro = Registro(
                id_trabajador=id_trabajador,
                hora_entrada=hora_entrada_completa
            )

            # Guarda el registro
            nuevo_registro.guardar()

            return {'message': 'Registro de entrada creado correctamente'}, HTTPStatus.CREATED

        except Exception as e:
            print(f"Error inesperado: {e}")
            return {'message': 'Error al procesar la solicitud'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @jwt_required()
    def put(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()  # Obtiene la identidad del usuario del token
        id_trabajador = int(current_user_id) # Convierte a int
        hora_salida_str = data.get('hora_salida')  # Recibe la hora como string

        if not id_trabajador or not hora_salida_str:
            return {'message': 'ID de trabajador y hora de salida son requeridos'}, HTTPStatus.BAD_REQUEST

        try:
            hora_salida = datetime.strptime(hora_salida_str, '%H:%M:%S')  # Convierte el string a datetime
        except ValueError:
            return {'message': 'Formato de hora de salida inválido. Use HH:MM:SS'}, HTTPStatus.BAD_REQUEST

        # Busca el registro más reciente para este trabajador sin hora de salida
        registro = Registro.query.filter_by(id_trabajador=id_trabajador, hora_salida=None).order_by(Registro.fecha.desc(),Registro.hora_entrada.desc()).first()

        if not registro:
            return {'message': 'Registro de entrada no encontrado o ya tiene hora de salida'}, HTTPStatus.NOT_FOUND

        # Actualiza la hora de salida
        now = datetime.utcnow()
        fecha_actual = now.date()
        hora_salida_completa = datetime.combine(fecha_actual, hora_salida.time())
        registro.hora_salida = hora_salida_completa
        db.session.commit()

        return {'message': 'Hora de salida registrada correctamente'}, HTTPStatus.OK

    @jwt_required()
    def get(self, id_trabajador):
        current_user_id = get_jwt_identity()  # Obtiene la identidad del usuario del token

        # Autorización: Verifica que el usuario autenticado sea el mismo que el trabajador solicitado
        if int(current_user_id) != id_trabajador:
            return {'message': 'No tiene permiso para acceder a este recurso'}, HTTPStatus.FORBIDDEN

        registros = Registro.query.filter_by(id_trabajador=id_trabajador).all()

        if registros:
            registros_list = []
            for registro in registros:
                registros_list.append({
                    'fecha': registro.fecha.strftime('%Y-%m-%d'),
                    'hora_entrada': registro.hora_entrada.strftime('%H:%M:%S') if registro.hora_entrada else None,
                    'hora_salida': registro.hora_salida.strftime('%H:%M:%S') if registro.hora_salida else None
                })
            return {'registros': registros_list}, HTTPStatus.OK
        else:
            return {'message': 'No hay registros'}, HTTPStatus.OK