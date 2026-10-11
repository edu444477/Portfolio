from flask_restful import Resource


class HealthResource(Resource):
    """Healthcheck para Render.

    No toca la base de datos a proposito: si la BD cae, el proceso sigue vivo y
    el servicio no debe reiniciarse en bucle. El estado real de la BD se
    comprueba en /api/health/db.
    """

    def get(self):
        return {'status': 'ok'}, 200
