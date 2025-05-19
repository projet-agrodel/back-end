from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('orders', __name__, url_prefix='/api')
controller = MainController()

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