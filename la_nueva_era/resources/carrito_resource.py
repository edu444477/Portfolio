from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, CarritoItem, Producto, Usuario
from decimal import Decimal

add_to_cart_parser = reqparse.RequestParser()
add_to_cart_parser.add_argument('idProducto', type=int, required=True, help="ID del producto es obligatorio.", location='json')

class CarritoResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        carrito_items_db = db.session.query(CarritoItem, Producto)\
            .join(Producto, CarritoItem.idProducto == Producto.idProducto)\
            .filter(CarritoItem.idUsuario == user_id)\
            .all()

        if not carrito_items_db:
            return {'message': 'Tu carrito está vacío', 'items': [], 'total_carrito': 0.0, 'cantidad_total_items': 0}, 200

        items_serializados = []
        total_carrito_valor_decimal = Decimal('0.00')
        cantidad_total_items = 0

        for item_carrito, producto in carrito_items_db:
            precio_unitario_decimal = producto.precio
            
            cantidad_en_carrito_item = Decimal(item_carrito.numProductos) 
            
            subtotal_item_decimal = precio_unitario_decimal * cantidad_en_carrito_item

            items_serializados.append({
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'precio_unitario': float(precio_unitario_decimal),
                'cantidad': int(cantidad_en_carrito_item),
                'subtotal': float(subtotal_item_decimal),
                'foto': producto.foto,
                'stock_disponible': producto.stock if hasattr(producto, 'stock') else None
            })
            total_carrito_valor_decimal += subtotal_item_decimal
            cantidad_total_items += int(cantidad_en_carrito_item)

        return {
            'items': items_serializados,
            'total_carrito': float(total_carrito_valor_decimal),
            'cantidad_total_items': cantidad_total_items
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = add_to_cart_parser.parse_args()

        producto_id = args['idProducto']
        cantidad_a_anadir_decimal = Decimal('1')

        producto = Producto.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        precio_producto_decimal = producto.precio # Asumiendo que producto.precio ya es Decimal

        if hasattr(producto, 'stock') and producto.stock < 1:
            return {'message': f'No hay stock disponible para {producto.nombre}.'}, 409

        item_carrito_existente = CarritoItem.query.filter_by(idUsuario=user_id, idProducto=producto_id).first()

        if item_carrito_existente:
            return {'message': f'"{producto.nombre}" ya está en tu carrito.'}, 409

        valor_item_decimal = precio_producto_decimal * cantidad_a_anadir_decimal
        
        nuevo_item_carrito = CarritoItem(
            idUsuario=user_id,
            idProducto=producto_id,
            numProductos=int(cantidad_a_anadir_decimal),
            valor=valor_item_decimal
        )
        db.session.add(nuevo_item_carrito)

        try:
            db.session.commit()
            return {'message': f'"{producto.nombre}" añadido al carrito'}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error POST /api/carrito: {e}")
            return {'message': 'Error al añadir producto al carrito'}, 500


class CarritoItemResource(Resource):
    @jwt_required()
    def delete(self, producto_id):
        user_id = get_jwt_identity()
        item_carrito = CarritoItem.query.filter_by(idUsuario=user_id, idProducto=producto_id).first()

        if not item_carrito:
            return {'message': 'Producto no encontrado en el carrito'}, 404

        nombre_producto_eliminado = "Producto"
        producto = Producto.query.get(producto_id)
        if producto:
            nombre_producto_eliminado = producto.nombre

        db.session.delete(item_carrito)
        try:
            db.session.commit()
            return {'message': f'"{nombre_producto_eliminado}" eliminado del carrito'}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error DELETE /api/carrito/item/{producto_id}: {e}")
            return {'message': 'Error al eliminar producto del carrito'}, 500