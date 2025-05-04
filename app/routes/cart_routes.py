from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('carts', __name__)
controller = MainController()

@bp.route('/cart', methods=['GET'])
def get_cart() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        cart_items = controller.carts.get_cart_items(user_id)
        return jsonify([item.to_dict() for item in cart_items]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/add', methods=['POST'])
def add_to_cart() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({'message': 'ID do produto é obrigatório'}), 400
            
        cart_item = controller.carts.add_item(user_id, product_id, quantity)
        return jsonify({'message': 'Item adicionado ao carrinho com sucesso'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/remove/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        result = controller.carts.remove_item(user_id, product_id)
        
        if result:
            return jsonify({'message': 'Item removido do carrinho com sucesso'}), 200
        return jsonify({'message': 'Item não encontrado no carrinho'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500 