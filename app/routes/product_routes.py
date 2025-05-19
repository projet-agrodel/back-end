from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('products', __name__)
controller = MainController()

@bp.route('/products', methods=['POST'])
def create_product() -> tuple[Any, int]:
    try:
        data = request.get_json()
        product = controller.products.create_product(data)
        return jsonify(product.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products', methods=['GET'])
def get_products() -> tuple[Any, int]:
    query = request.args.get('q')
    min_price_str = request.args.get('minPrice')
    max_price_str = request.args.get('maxPrice')
    sort = request.args.get('sort')

    min_price = None
    if min_price_str:
        try:
            min_price = float(min_price_str)
        except ValueError:
            return jsonify({'error': "Parâmetro 'minPrice' inválido."}), 400
            
    max_price = None
    if max_price_str:
        try:
            max_price = float(max_price_str)
        except ValueError:
            return jsonify({'error': "Parâmetro 'maxPrice' inválido."}), 400

    try:
        products = controller.products.get_all(
            query=query, 
            min_price=min_price, 
            max_price=max_price, 
            sort=sort
        )
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({'error': "Erro interno ao buscar produtos."}), 500

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int) -> tuple[Any, int]:
    product = controller.products.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    return jsonify(product.to_dict()), 200

@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        product = controller.products.update_product(product_id, data)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<int:product_id>/stock', methods=['PATCH'])
def update_stock(product_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        quantity = data.get('quantity', 0)
        product = controller.products.update_stock(product_id, quantity)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int) -> tuple[Any, int]:
    try:
        if controller.products.delete(product_id):
            return jsonify({'message': 'Produto deletado com sucesso'}), 200
        return jsonify({'error': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400 