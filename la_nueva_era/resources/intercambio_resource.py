from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Usuario, Producto, InventarioItem
import decimal

intercambio_parser = reqparse.RequestParser()
intercambio_parser.add_argument('ids_productos_dar', type=list, location='json', required=True, help='Lista de IDs de productos a dar es requerida')
intercambio_parser.add_argument('ids_productos_recibir', type=list, location='json', required=True, help='Lista de IDs de productos a recibir es requerida')

class IntercambioResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        args = intercambio_parser.parse_args()

        ids_dar_str = args['ids_productos_dar']
        ids_recibir_str = args['ids_productos_recibir']

        if not ids_dar_str or not ids_recibir_str:
            return {"message": "Debes seleccionar artículos tanto para dar como para recibir."}, 400

        try:
            ids_productos_dar = [int(pid) for pid in ids_dar_str]
            ids_productos_recibir = [int(pid) for pid in ids_recibir_str]
        except ValueError:
            return {"message": "IDs de producto inválidos."}, 400

        usuario = Usuario.query.get(current_user_id)
        if not usuario:
            return {"message": "Usuario no autenticado."}, 401

        for producto_id_recibir_check in ids_productos_recibir:
            item_ya_en_inventario = InventarioItem.query.filter_by(
                idUsuario=current_user_id,
                idProducto=producto_id_recibir_check
            ).first()
            if item_ya_en_inventario:
                producto_existente = Producto.query.get(producto_id_recibir_check)
                nombre_producto_existente = producto_existente.nombre if producto_existente else f"ID {producto_id_recibir_check}"
                return {
                    "message": f"No puedes recibir '{nombre_producto_existente}' porque ya lo tienes en tu inventario y los artículos se tratan como únicos en el intercambio."
                }, 409

        valor_total_dados = decimal.Decimal(0.0)
        items_inventario_a_eliminar = []

        for producto_id_dar in ids_productos_dar:
            item_inventario = InventarioItem.query.filter_by(idUsuario=current_user_id, idProducto=producto_id_dar).first()
            if not item_inventario:
                return {"message": f"No posees el artículo con ID {producto_id_dar} para dar o ya no está en tu inventario."}, 404

            producto_dado = Producto.query.get(producto_id_dar)
            if not producto_dado:
                 return {"message": f"Error al encontrar detalles del producto a dar con ID {producto_id_dar}."}, 500

            if item_inventario.numProductos < 1:
                 return {"message": f"No tienes suficientes unidades del artículo {producto_dado.nombre} para dar."}, 400

            valor_total_dados += decimal.Decimal(producto_dado.precio)
            items_inventario_a_eliminar.append(item_inventario)


        valor_total_recibidos = decimal.Decimal(0.0)
        productos_a_recibir_info = []

        for producto_id_recibir in ids_productos_recibir:
            producto_tienda = Producto.query.get(producto_id_recibir)
            if not producto_tienda:
                return {"message": f"El artículo con ID {producto_id_recibir} que quieres recibir no existe."}, 404

            valor_total_recibidos += decimal.Decimal(producto_tienda.precio)
            productos_a_recibir_info.append(producto_tienda)

        if valor_total_dados < valor_total_recibidos:
            return {"message": "El valor de los artículos que ofreces ({:.2f}€) es menor que el valor de los artículos que deseas recibir ({:.2f}€).".format(valor_total_dados, valor_total_recibidos)}, 402

        # Iniciar transacción
        try:
            # 1. Eliminar items dados del inventario del usuario
            for item_inv in items_inventario_a_eliminar:
                db.session.delete(item_inv)

            # 2. Añadir items recibidos al inventario del usuario
            for prod_recibir in productos_a_recibir_info:
                # Verificar si el usuario ya tiene este producto para incrementar cantidad, o crear nuevo
                item_existente_inventario = InventarioItem.query.filter_by(idUsuario=current_user_id, idProducto=prod_recibir.idProducto).first()
                if item_existente_inventario:
                    item_existente_inventario.numProductos += 1
                    item_existente_inventario.valor = prod_recibir.precio
                else:
                    nuevo_item_inventario = InventarioItem(
                        idUsuario=current_user_id,
                        idProducto=prod_recibir.idProducto,
                        numProductos=1,
                        valor=prod_recibir.precio
                    )
                    db.session.add(nuevo_item_inventario)

            db.session.commit()
            return {"message": "¡Intercambio realizado con éxito!"}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error en transacción de intercambio: {e}")
            return {"message": "Error interno al procesar el intercambio."}, 500














