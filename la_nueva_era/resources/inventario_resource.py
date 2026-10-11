from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from models import db, Usuario, Producto, InventarioItem, Categoria, Juego

# Parser para los argumentos de la query (filtros y paginación)
inventario_parser = reqparse.RequestParser()
inventario_parser.add_argument('page', type=int, default=1, location='args')
inventario_parser.add_argument('per_page', type=int, default=12, location='args')
inventario_parser.add_argument('categoria_id', type=int, location='args')
inventario_parser.add_argument('calidad', type=str, location='args')
inventario_parser.add_argument('juego_ids', type=str, location='args')
inventario_parser.add_argument('sort_by', type=str, default='nombre', location='args')
inventario_parser.add_argument('order', type=str, default='asc', location='args')
inventario_parser.add_argument('precio_min', type=float, location='args')
inventario_parser.add_argument('precio_max', type=float, location='args')


class InventarioUsuarioResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        args = inventario_parser.parse_args()

        query = db.session.query(InventarioItem, Producto, Categoria, Juego)\
            .join(Producto, InventarioItem.idProducto == Producto.idProducto)\
            .join(Categoria, Producto.idCategoria == Categoria.idCategoria)\
            .join(Juego, Producto.idJuego == Juego.idJuego)\
            .filter(InventarioItem.idUsuario == current_user_id)

        # Aplicar filtros
        if args['categoria_id']:
            query = query.filter(Producto.idCategoria == args['categoria_id'])
        if args['calidad']:
            query = query.filter(Producto.calidad == args['calidad'])

        if args['juego_ids']:
            juego_ids_list = [int(gid.strip()) for gid in args['juego_ids'].split(',') if gid.strip().isdigit()]
            if juego_ids_list:
                query = query.filter(Producto.idJuego.in_(juego_ids_list))

        if args['precio_min'] is not None:
            query = query.filter(Producto.precio >= args['precio_min'])
        if args['precio_max'] is not None:
            query = query.filter(Producto.precio <= args['precio_max'])

        # Ordenamiento
        if args['sort_by'] == 'precio':
            order_column = Producto.precio
        elif args['sort_by'] == 'nombre':
            order_column = Producto.nombre
        else:
            order_column = Producto.nombre

        if args['order'] == 'desc':
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        # Paginación
        page = args['page']
        per_page = args['per_page']

        # Contar total de items antes de paginar para la metadata
        # Clonamos la query para no afectar el ordenamiento y paginación principal
        total_items_query = query.statement.with_only_columns(func.count()).order_by(None)
        total_items = db.session.execute(total_items_query).scalar_one()

        total_paginas = (total_items + per_page - 1) // per_page # Cálculo de total de páginas

        inventario_paginado = query.paginate(page=page, per_page=per_page, error_out=False)

        resultados = []
        for item_inventario, producto, categoria, juego in inventario_paginado.items:
            resultados.append({
                'idInventarioItem': f"{item_inventario.idUsuario}-{item_inventario.idProducto}",
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'calidad': producto.calidad,
                'precio': float(producto.precio),
                'foto': producto.foto,
                'stock_usuario': item_inventario.numProductos,
                'categoria_nombre': categoria.nombre,
                'juego_nombre': juego.nombre,
            })

        return {
            'productos': resultados,
            'pagina_actual': inventario_paginado.page,
            'total_paginas': total_paginas,
            'total_items': total_items,
            'por_pagina': inventario_paginado.per_page
        }, 200

# Parser para el cuerpo de la petición del método POST
vender_parser = reqparse.RequestParser()
vender_parser.add_argument('id_productos_a_vender',
                           type=list,
                           location='json',
                           required=True,
                           help="Lista de IDs de producto a vender es requerida")

class VenderItemsResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()

        args = vender_parser.parse_args()
        id_productos_para_vender = args['id_productos_a_vender']

        if not id_productos_para_vender:
            return {"msg": "No se proporcionaron IDs de producto para vender"}, 400

        usuario = Usuario.query.get(current_user_id)
        if not usuario:
            return {"msg": "Usuario no encontrado"}, 404

        total_valor_venta_acumulado = 0
        items_vendidos_info = []

        try:
            for id_producto in id_productos_para_vender:
                try:
                    id_producto_int = int(id_producto)
                except (ValueError, TypeError):
                    db.session.rollback()
                    return {"msg": f"ID de producto inválido proporcionado: {id_producto}"}, 400

                # Buscar el item en el inventario del usuario
                item_inventario = InventarioItem.query.filter_by(
                    idUsuario=current_user_id,
                    idProducto=id_producto_int
                ).first()

                if not item_inventario:
                    db.session.rollback()
                    return {"msg": f"Producto con ID {id_producto_int} no encontrado en tu inventario o ya fue vendido."}, 404

                if item_inventario.valor is None:
                    db.session.rollback()
                    return {"msg": f"Información de valor incompleta para el producto con ID {id_producto_int}."}, 500

                valor_de_este_item = item_inventario.valor
                total_valor_venta_acumulado += valor_de_este_item

                db.session.delete(item_inventario)

                items_vendidos_info.append({
                    "idProducto": id_producto_int,
                    "cantidad_vendida": item_inventario.numProductos, # Debería ser 1
                    "valor_obtenido": float(valor_de_este_item)
                })

            # Actualizar el saldo del usuario
            usuario.saldo += total_valor_venta_acumulado

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error durante la venta de items: {e}") # Log para depuración
            return {"msg": "Ocurrió un error durante el proceso de venta. Inténtalo de nuevo."}, 500

        return {
            "msg": "Artículo vendido exitosamente.",
            "saldo_actual": float(usuario.saldo),
            "total_obtenido_transaccion": float(total_valor_venta_acumulado),
            "items_procesados": items_vendidos_info
        }, 200















