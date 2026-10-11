from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Pedido, DetallePedido, CarritoItem, Producto, Usuario, InventarioItem
from datetime import date
import decimal

pedido_parser = reqparse.RequestParser()
pedido_parser.add_argument('id_productos_seleccionados', type=list, location='json', required=True, help="Se requiere una lista de IDs de productos seleccionados.")

class PedidoResource(Resource):
    @jwt_required()
    def post(self):
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)
        usuario = Usuario.query.get(user_id)

        args = pedido_parser.parse_args()
        id_productos_seleccionados = args.get('id_productos_seleccionados')

        if not id_productos_seleccionados:
            return {'message': 'No se seleccionaron productos para la compra.'}, 400

        # 1. Obtener SOLAMENTE los items del carrito que fueron SELECCIONADOS por el usuario y que pertenecen al usuario actual.
        carrito_items_db = db.session.query(CarritoItem, Producto)\
            .join(Producto, CarritoItem.idProducto == Producto.idProducto)\
            .filter(CarritoItem.idUsuario == user_id)\
            .filter(CarritoItem.idProducto.in_(id_productos_seleccionados))\
            .all()

        if not carrito_items_db:
            return {'message': 'Los productos seleccionados no se encontraron en tu carrito o el carrito está vacío.'}, 400

        total_pedido = decimal.Decimal(0.0)
        detalles_pedido_para_crear = []
        productos_ids_en_pedido = []
        productos_ya_en_inventario_nombres = []

        # 2. Validar stock, SI EL PRODUCTO YA ESTÁ EN EL INVENTARIO, y calcular total
        for item_carrito, producto in carrito_items_db:
            cantidad_comprada_de_este_producto = 1
            
            # 2.a VERIFICAR SI EL PRODUCTO YA ESTÁ EN EL INVENTARIO DEL USUARIO
            item_ya_en_inventario = InventarioItem.query.filter_by(
                idUsuario=user_id,
                idProducto=producto.idProducto
            ).first()

            if item_ya_en_inventario:
                productos_ya_en_inventario_nombres.append(producto.nombre)
                continue

            # 2.b Validación de stock
            if producto.stock < cantidad_comprada_de_este_producto:
                return {'message': f'Stock insuficiente para "{producto.nombre}".'}, 409

            subtotal_item_en_pedido = decimal.Decimal(producto.precio)
            total_pedido += subtotal_item_en_pedido
            
            detalles_pedido_para_crear.append({
                'producto_id': producto.idProducto,
                'cantidad_comprada': cantidad_comprada_de_este_producto, 
                'precio_unitario_compra': producto.precio,
                'subtotal_en_pedido': subtotal_item_en_pedido
            })
            productos_ids_en_pedido.append(producto.idProducto)

        if not detalles_pedido_para_crear and productos_ya_en_inventario_nombres:
             return {'message': f"Los siguientes productos seleccionados ya están en tu inventario y no se pueden comprar de nuevo: {', '.join(productos_ya_en_inventario_nombres)}. Por favor, elimínalos de la cesta para continuar con otros artículos, o vacía la cesta si solo contenía estos.", 'productos_duplicados': productos_ya_en_inventario_nombres}, 409 # 409 Conflict
        elif not detalles_pedido_para_crear:
            return {'message': 'No hay productos válidos para procesar en este pedido.'}, 400


        # 3. Verificar saldo del usuario
        if usuario.saldo < total_pedido:
            return {'message': f'Saldo insuficiente para los artículos válidos. Necesitas {total_pedido:.2f}€ y tienes {usuario.saldo:.2f}€.'}, 402

        # --- INICIO TRANSACCIÓN ---
        try:
            # 4. Descontar saldo del usuario
            usuario.saldo -= total_pedido

            # 5. Crear el Pedido
            nuevo_pedido = Pedido(
                idUsuario=user_id,
                total=total_pedido,
                fecha=date.today(),
                estado="Completado"
            )
            db.session.add(nuevo_pedido)
            db.session.flush() 

            # 6. Crear los Detalles del Pedido, descontar stock y añadir a InventarioItem
            for detalle_data in detalles_pedido_para_crear:
                # 6.a Crear DetallePedido
                detalle = DetallePedido(
                    idPedido=nuevo_pedido.idPedido,
                    idProducto=detalle_data['producto_id'],
                    numProductos=detalle_data['cantidad_comprada'],
                    valor=detalle_data['subtotal_en_pedido']
                )
                db.session.add(detalle)

                # 6.b Descontar stock del Producto
                producto_a_actualizar = Producto.query.get(detalle_data['producto_id'])
                if producto_a_actualizar:
                 producto_a_actualizar.stock -= detalle_data['cantidad_comprada']
                
                # 6.c Crear NUEVA entrada en InventarioItem
                nuevo_item_inventario = InventarioItem(
                    idUsuario=user_id,
                    idProducto=detalle_data['producto_id'],
                    numProductos=1,
                    valor=detalle_data['precio_unitario_compra'] 
                )
                db.session.add(nuevo_item_inventario)

            # 7. Vaciar SOLAMENTE los items comprados Y VÁLIDOS del carrito del usuario
            if productos_ids_en_pedido:
                CarritoItem.query.filter(
                    CarritoItem.idUsuario == user_id,
                    CarritoItem.idProducto.in_(productos_ids_en_pedido)
                ).delete(synchronize_session=False)

            db.session.commit()
            # --- FIN TRANSACCIÓN ---

            mensaje_final = '¡Compra realizada con éxito!'
            if productos_ya_en_inventario_nombres:
                mensaje_final += f" Los siguientes productos no se procesaron porque ya los posees: {', '.join(productos_ya_en_inventario_nombres)}."

            return {
                'message': mensaje_final,
                'idPedido': nuevo_pedido.idPedido,
                'total_pagado': float(total_pedido),
                'productos_no_procesados_por_duplicado': productos_ya_en_inventario_nombres if productos_ya_en_inventario_nombres else None
            }, 201

        except Exception as e:
            db.session.rollback()
            print(f"Error al procesar pedido para usuario {user_id}: {e}")
            return {'message': 'Error interno al procesar el pedido. Inténtalo de nuevo más tarde.'}, 500
            
            
            
            
            
            
            
            
