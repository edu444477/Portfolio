from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import db, Producto, Categoria, Juego, InventarioItem
from sqlalchemy import or_, and_

class ProductoListResource(Resource):
    def get(self):
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
        except Exception:
            current_user_id = None

        contexto_arg = request.args.get('contexto', type=str)

        query = db.session.query(Producto)

        if contexto_arg == 'intercambio_recibir' and current_user_id:
            subquery_inventario_usuario = db.session.query(InventarioItem.idProducto)\
                .filter(InventarioItem.idUsuario == current_user_id)\
                .subquery()

            query = query.filter(Producto.idProducto.notin_(subquery_inventario_usuario))

        categoria_id_arg = request.args.get('categoria_id', type=int)
        if categoria_id_arg:
            query = query.filter(Producto.idCategoria == categoria_id_arg)

        juego_id_arg = request.args.get('juego_id', type=int)
        if juego_id_arg:
            query = query.filter(Producto.idJuego == juego_id_arg)

        juego_ids_str = request.args.get('juego_ids', type=str)
        if juego_ids_str:
            try:
                juego_ids_list = [int(id_str.strip()) for id_str in juego_ids_str.split(',') if id_str.strip().isdigit()]
                if juego_ids_list:
                    query = query.filter(Producto.idJuego.in_(juego_ids_list))
            except ValueError:
                pass


        calidad_arg = request.args.get('calidad', type=str)
        if calidad_arg:
            query = query.filter(Producto.calidad == calidad_arg)

        en_stock_arg = request.args.get('en_stock', type=str)
        if en_stock_arg and en_stock_arg.lower() == 'true':
            if hasattr(Producto, 'stock'):
                query = query.filter(Producto.stock > 0)

        precio_min_arg = request.args.get('precio_min', type=float)
        if precio_min_arg is not None:
            query = query.filter(Producto.precio >= precio_min_arg)

        precio_max_arg = request.args.get('precio_max', type=float)
        if precio_max_arg is not None:
            query = query.filter(Producto.precio <= precio_max_arg)

        search_term_arg = request.args.get('q', type=str)
        if search_term_arg:
            search_pattern = f"%{search_term_arg}%"
            query = query.filter(or_(
                Producto.nombre.ilike(search_pattern),
            ))

        sort_by_arg = request.args.get('sort_by', type=str)
        order_arg = request.args.get('order', 'asc', type=str).lower()

        if not sort_by_arg or sort_by_arg == 'recomendado':
            query = query.order_by(Producto.idProducto.desc())
        else:
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

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)

        try:
            final_query = query.join(Categoria, Producto.idCategoria == Categoria.idCategoria)\
                               .join(Juego, Producto.idJuego == Juego.idJuego)\
                               .add_columns(
                                   Producto.idProducto,
                                   Producto.nombre,
                                   Producto.descripcion,
                                   Producto.calidad,
                                   Producto.precio,
                                   Producto.foto,
                                   Producto.stock,
                                   Categoria.nombre.label('categoria_nombre'),
                                   Juego.nombre.label('juego_nombre')
                                )

            paginated_result = final_query.paginate(page=page, per_page=per_page, error_out=False)
            productos_data_list = paginated_result.items

            response_productos = []
            for row in productos_data_list:
                response_productos.append({
                    'idProducto': row.idProducto,
                    'nombre': row.nombre,
                    'descripcion': row.descripcion,
                    'calidad': row.calidad,
                    'precio': float(row.precio) if row.precio is not None else None,
                    'foto': row.foto,
                    'stock': row.stock,
                    'categoria_nombre': row.categoria_nombre,
                    'juego_nombre': row.juego_nombre,
                })

            response_data = {
                'productos': response_productos,
                'total_items': paginated_result.total,
                'pagina_actual': paginated_result.page,
                'total_paginas': paginated_result.pages,
                'por_pagina': paginated_result.per_page
            }
            return response_data, 200

        except Exception as e:
            print(f"Error al obtener productos: {e}")
            db.session.rollback()
            return {'message': 'Error interno al obtener productos.'}, 500

class ProductoResource(Resource):
    def get(self, producto_id):
        producto_info = db.session.query(
            Producto,
            Categoria.nombre.label('categoria_nombre'),
            Juego.nombre.label('juego_nombre')
        )\
        .join(Categoria, Producto.idCategoria == Categoria.idCategoria)\
        .join(Juego, Producto.idJuego == Juego.idJuego)\
        .filter(Producto.idProducto == producto_id)\
        .first()

        if not producto_info:
            return {'message': 'Producto no encontrado'}, 404

        producto, categoria_nombre, juego_nombre = producto_info

        return {
            'idProducto': producto.idProducto,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'calidad': producto.calidad,
            'precio': float(producto.precio),
            'foto': producto.foto,
            'stock': producto.stock,
            'idCategoria': producto.idCategoria,
            'categoria_nombre': categoria_nombre,
            'idJuego': producto.idJuego,
            'juego_nombre': juego_nombre,
        }, 200

class CategoriaListResource(Resource):
    def get(self):
        try:
            categorias = Categoria.query.all()
            return [categoria.to_dict() for categoria in categorias], 200
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return {'message': 'Error interno al obtener categorías'}, 500

class JuegoListResource(Resource):
    def get(self):
        try:
            juegos = Juego.query.all()
            return [juego.to_dict() for juego in juegos], 200
        except Exception as e:
            print(f"Error al obtener juegos: {e}")
            return {'message': 'Error interno al obtener juegos'}, 500
















