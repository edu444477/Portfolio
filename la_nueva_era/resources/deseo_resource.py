from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import db, DeseoItem, Producto, Usuario

deseo_parser = reqparse.RequestParser()
deseo_parser.add_argument('idProducto', type=int, required=True, help="ID del producto es obligatorio.", location='json')

class DeseoListResource(Resource):
    @jwt_required()
    def get(self):
        user_id_from_token = get_jwt_identity()
        try:
            user_id = int(user_id_from_token)
        except ValueError:
            return {'message': 'Token de usuario inválido'}, 400

        # 1. Obtener solo los IDs de los productos en la lista de deseos del usuario
        producto_ids_en_deseos = db.session.query(DeseoItem.idProducto)\
                                          .filter(DeseoItem.idUsuario == user_id)\
                                          .distinct()\
                                          .all()

        # Convertir la lista de tuplas a una lista de IDs planos
        lista_ids_productos_deseados = [pid[0] for pid in producto_ids_en_deseos]

        if not lista_ids_productos_deseados:
            return {
                'message': 'Tu lista de deseos está vacía.',
                'productos': [],
                'total_productos': 0,
                'pagina_actual': 1,
                'total_paginas': 0,
                'por_pagina': request.args.get('per_page', 12, type=int)
            }, 200

        # 2. Construir la query sobre la tabla Producto, filtrando por esos IDs
        query = Producto.query.filter(Producto.idProducto.in_(lista_ids_productos_deseados))

        # --- Aplicar Filtros ---
        categoria_id_arg = request.args.get('categoria_id', type=int)
        if categoria_id_arg:
            query = query.filter(Producto.idCategoria == categoria_id_arg)

        calidad_arg = request.args.get('calidad', type=str)
        if calidad_arg:
            query = query.filter(Producto.calidad == calidad_arg)

        en_stock_arg = request.args.get('en_stock', type=str)
        if en_stock_arg and en_stock_arg.lower() == 'true':
            query = query.filter(Producto.stock > 0)

        precio_min_arg = request.args.get('precio_min', type=float)
        if precio_min_arg is not None:
            query = query.filter(Producto.precio >= precio_min_arg)

        precio_max_arg = request.args.get('precio_max', type=float)
        if precio_max_arg is not None:
            query = query.filter(Producto.precio <= precio_max_arg)

        juego_ids_str = request.args.get('juego_ids', type=str)
        if juego_ids_str:
            try:
                juego_ids_list = [int(id_str.strip()) for id_str in juego_ids_str.split(',') if id_str.strip().isdigit()]
                if juego_ids_list:
                    query = query.filter(Producto.idJuego.in_(juego_ids_list))
            except ValueError:
                print(f"Advertencia GET /api/deseos (juego_ids): formato incorrecto: {juego_ids_str}")
                pass

        # --- Aplicar Ordenación ---
        sort_by_arg = request.args.get('sort_by', type=str)
        order_arg = request.args.get('order', 'asc', type=str).lower()

        if sort_by_arg and sort_by_arg != "recomendado":
            column_to_sort = None
            if sort_by_arg == 'precio':
                column_to_sort = Producto.precio
            elif sort_by_arg == 'nombre':
                column_to_sort = Producto.nombre
            elif sort_by_arg == 'calidad':
                column_to_sort = Producto.calidad

            if column_to_sort is not None:
                if order_arg == 'desc':
                    query = query.order_by(column_to_sort.desc())
                else:
                    query = query.order_by(column_to_sort.asc())
            else: # Fallback si sort_by no es conocido
                query = query.order_by(Producto.nombre.asc())
        else: # Orden por defecto
            query = query.order_by(Producto.nombre.asc())

        # --- Paginación ---
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        try:
            paginated_productos_deseados = query.paginate(page=page, per_page=per_page, error_out=False)
            productos_list = paginated_productos_deseados.items

            response_data = {
                'productos': [producto.to_dict() for producto in productos_list],
                'total_productos': paginated_productos_deseados.total,
                'pagina_actual': paginated_productos_deseados.page,
                'total_paginas': paginated_productos_deseados.pages,
                'por_pagina': paginated_productos_deseados.per_page,
            }
            return response_data, 200

        except Exception as e:
            print(f"Error al obtener lista de deseos: {e}")
            return {'message': f'Error interno al obtener lista de deseos: {str(e)}'}, 500

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = deseo_parser.parse_args()
        producto_id = args['idProducto']

        # Verificar que el producto existe
        producto = Producto.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        # Verificar si ya está en la lista de deseos
        existente = DeseoItem.query.filter_by(idUsuario=user_id, idProducto=producto_id).first()
        if existente:
            return {'message': f'"{producto.nombre}" ya está en tu lista de deseos'}, 200 # O 409 Conflict si prefieres

        nuevo_deseo = DeseoItem(
            idUsuario=user_id,
            idProducto=producto_id,
            nombre=producto.nombre,
            numProductos=1
        )
        db.session.add(nuevo_deseo)
        try:
            db.session.commit()
            return {'message': f'"{producto.nombre}" añadido a tu lista de deseos', 'idDeseo': nuevo_deseo.idDeseo}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error POST /api/deseos: {e}")
            return {'message': 'Error al añadir a la lista de deseos'}, 500


class DeseoItemResource(Resource):
    @jwt_required()
    def delete(self, producto_id):
        user_id = get_jwt_identity()

        deseo_item = DeseoItem.query.filter_by(idUsuario=user_id, idProducto=producto_id).first()
        if not deseo_item:
            return {'message': 'Este producto no está en tu lista de deseos o ya fue eliminado'}, 404

        nombre_producto = "Producto"
        if deseo_item.producto:
            nombre_producto = deseo_item.producto.nombre

        db.session.delete(deseo_item)
        try:
            db.session.commit()
            return {'message': f'"{nombre_producto}" eliminado de tu lista de deseos'}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error DELETE /api/deseos/{producto_id}: {e}")
            return {'message': 'Error al eliminar de la lista de deseos'}, 500

class DeseoIDsResource(Resource):
    @jwt_required()
    def get(self):
        user_id_from_token = get_jwt_identity()
        try:
            user_id = int(user_id_from_token)
        except (ValueError, TypeError):
            return {'message': 'Token de usuario inválido'}, 400

        try:
            producto_ids_query = db.session.query(DeseoItem.idProducto).filter(DeseoItem.idUsuario == user_id).all()

            lista_ids = [item[0] for item in producto_ids_query]

            return {'wishlist_ids': lista_ids}, 200

        except Exception as e:
            print(f"Error al obtener los IDs de la lista de deseos: {e}")
            return {'message': 'Error interno al procesar la solicitud'}, 500














