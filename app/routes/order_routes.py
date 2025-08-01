from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from app.services.email_service import send_new_order_notification
from typing import Any

bp = Blueprint('orders', __name__, url_prefix='/api')
controller = MainController()

order_bp = Blueprint('order_bp', __name__, url_prefix='/admin/orders')

@bp.route('/orders', methods=['POST'])
def create_order() -> tuple[Any, int]:
    try:
        data = request.get_json()
        order = controller.orders.create_order(
            user_id=data.get('user_id'),
            items=data.get('items', []),
            description=data.get('description', '')
        )
        
        # Envia a notificação de e-mail após o pedido ser criado com sucesso
        send_new_order_notification(order)

        return jsonify({'message': 'Pedido criado com sucesso', 'order': order.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders', methods=['GET'])
def get_user_orders() -> tuple[Any, int]:
    try:
        # Parâmetros de busca
        status = request.args.get('status')
        search = request.args.get('search')
        user_id = request.args.get('user_id', type=int)
    
        orders = controller.orders.search_orders(
            user_id=user_id,
            status=status,
            search_term=search,
            is_admin=True
        )
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/all', methods=['GET'])
def get_orders() -> tuple[Any, int]:
    try:
        orders = controller.orders.get_all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id: int) -> tuple[Any, int]:
    try:
        user_id = request.args.get('user_id', type=int)
        order = controller.orders.get_order_with_items_and_check_permission(order_id, user_id, is_admin=True)
        if not order:
            return jsonify({'message': 'Pedido não encontrado ou acesso negado'}), 404
        return jsonify(order.to_dict()), 200
    except PermissionError as e:
        return jsonify({'message': str(e)}), 403
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id: int) -> tuple[Any, int]:
    try:
        user_id = 1
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'message': 'Status do pedido é obrigatório'}), 400
            
        order = controller.orders.update_order_status(
            order_id=order_id,
            status=data['status'],
            user_id=user_id,
            is_admin=True
        )
        
        if not order:
            return jsonify({'message': 'Pedido não encontrado ou acesso negado'}), 404
            
        return jsonify({
            'message': 'Status do pedido atualizado com sucesso',
            'order': order.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except PermissionError as e:
        return jsonify({'message': str(e)}), 403
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        is_admin = controller.users.get_by_id(user_id).type == 'admin'
        
        if controller.orders.delete_order(order_id, user_id, is_admin):
            return jsonify({'message': 'Pedido excluído com sucesso'}), 200
        return jsonify({'message': 'Pedido não encontrado ou acesso negado'}), 404
    except PermissionError as e:
        return jsonify({'message': str(e)}), 403
    except Exception as e:
        return jsonify({'message': str(e)}), 500 
