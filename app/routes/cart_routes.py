from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('carts', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        cart_items = controller.carts.get_cart_items(user_id)
        return jsonify([item.to_dict() for item in cart_items]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/item', methods=['POST'])
@jwt_required()
def add_item_to_cart() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        produto_id = data.get('produto_id')
        quantity = data.get('quantity', 1)
        
        if not produto_id:
            return jsonify({'message': 'ID do produto é obrigatório'}), 400
            
        try:
            cart_item = controller.carts.add_item(user_id, produto_id, quantity)
            return jsonify(cart_item.to_dict()), 201
        except ValueError as e:
            if "maior que estoque disponível" in str(e):
                return jsonify({'message': str(e)}), 409  # Conflict - estoque insuficiente
            raise
            
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/item/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(product_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({'message': 'Quantidade é obrigatória'}), 400

        controller.carts.remove_item(user_id, product_id)

        try:
            cart_item = controller.carts.add_item(user_id, product_id, quantity)
            return jsonify(cart_item.to_dict()), 200
        except ValueError as e:
            if "maior que estoque disponível" in str(e):
                return jsonify({'message': str(e)}), 409  # Conflict - estoque insuficiente
            raise
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/item/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_item_from_cart(product_id: int) -> tuple[Any, int]:
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

@bp.route('/cart', methods=['DELETE'])
@jwt_required()
def clear_cart() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        cart = controller.carts.get_or_create_cart(user_id)
        
        # Remover todos os itens do carrinho
        from app.models.cart import CartItem
        CartItem.query.filter_by(carrinho_id=cart.id).delete()
        controller._db.session.commit()
        
        return jsonify({'message': 'Carrinho esvaziado com sucesso'}), 200
    except Exception as e:
        controller._db.session.rollback()
        return jsonify({'message': str(e)}), 500

@bp.route('/cart/sync', methods=['POST'])
@jwt_required()
def sync_cart() -> tuple[Any, int]:
    """
    Sincroniza o carrinho local do usuário com o carrinho do backend após login.
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'items' not in data or not isinstance(data['items'], list):
            return jsonify({'message': 'Formato de dados inválido. Esperado: {"items": [...]}'}), 400

        synced_items = controller.carts.sync_cart(user_id, data['items'])
        
        return jsonify({
            'message': 'Carrinho sincronizado com sucesso',
            'items': [item.to_dict() for item in synced_items]
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Erro ao sincronizar carrinho: {str(e)}'}), 500 