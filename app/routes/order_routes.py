from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any
from app.controllers.order_controller import OrderController


bp = Blueprint('orders', __name__, url_prefix='/api')
controller = MainController()

order_bp = Blueprint('order_bp', __name__, url_prefix='/admin/orders')

@bp.route('/orders', methods=['POST'])

@jwt_required()
def create_order() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        order = controller.orders.create_order(
            user_id=user_id,
            items=data.get('items', []),
            description=data.get('description', '')
        )
        return jsonify({'message': 'Pedido criado com sucesso', 'order': order.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        orders = controller.orders.get_user_orders(user_id)
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['GET'])

@jwt_required()
def get_order_details(order_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        order = controller.orders.get_order_with_items_and_check_permission(order_id, user_id, is_admin=False)
        if not order:
            return jsonify({'message': 'Pedido não encontrado ou acesso negado'}), 404
        return jsonify(order.to_dict()), 200
    except PermissionError as e:
        return jsonify({'message': str(e)}), 403
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@order_bp.route('', methods=['GET'])
# @admin_required()
def get_orders_route():
    return OrderController.get_orders()

@order_bp.route('/<string:order_id>', methods=['GET'])
# @admin_required()
def get_order_route(order_id):
    return OrderController.get_order_by_id(order_id)

@order_bp.route('/<string:order_id>/status', methods=['PATCH'])
# @admin_required()
def update_order_status_route(order_id):
    return OrderController.update_order_status(order_id)

# Exemplo de como seriam outras rotas, se implementadas no controller:
# @order_bp.route('', methods=['POST'])
# # @admin_required()
# def create_order_route():
#     return OrderController.create_order()

# @order_bp.route('/<string:order_id>', methods=['DELETE'])
# # @admin_required()
# def delete_order_route(order_id):
#     return OrderController.delete_order() 