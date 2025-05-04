from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('orders', __name__)
controller = MainController()

@bp.route('/orders', methods=['POST'])
def create_order() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        order = controller.orders.create_order(
            user_id=user_id,
            items=data.get('items', []),
            description=data.get('description', '')
        )
        return jsonify({'message': 'Pedido criado com sucesso', 'id': order.id}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders', methods=['GET'])
def get_user_orders() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        orders = controller.orders.get_user_orders(user_id)
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id: int) -> tuple[Any, int]:
    try:
        order = controller.orders.get_order_with_items(order_id)
        if not order:
            return jsonify({'message': 'Pedido não encontrado'}), 404
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500 