from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.incidencia import Incidencia
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

class IncidenciaResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()  # Obtiene la identidad del usuario del token
        id_trabajador = int(current_user_id) # Convierte a int
        descripcion = data.get('descripcion')
        fecha_str = data.get('fecha')

        if not id_trabajador or not descripcion:
            return {'message': 'ID de trabajador y descripción son requeridos'}, HTTPStatus.BAD_REQUEST

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS'}, HTTPStatus.BAD_REQUEST

        nueva_incidencia = Incidencia(
            id_trabajador=id_trabajador,
            descripcion=descripcion,
            fecha=fecha
        )

        nueva_incidencia.guardar()

        return {'message': 'Incidencia registrada correctamente'}, HTTPStatus.CREATED

    @jwt_required()
    def get(self, id_trabajador):
        incidencias = Incidencia.query.filter_by(id_trabajador=id_trabajador).all()

        if incidencias:
            incidencias_list = []
            for incidencia in incidencias:
                incidencias_list.append({
                    'fecha': incidencia.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    'descripcion': incidencia.descripcion
                })
            return {'incidencias': incidencias_list}, HTTPStatus.OK
        else:
            return {'message': 'No hay incidencias'}, HTTPStatus.OK