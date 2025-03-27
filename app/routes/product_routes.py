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
    query = request.args.get('query')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    in_stock = request.args.get('in_stock')

    if query:
        products = controller.products.search_products(query)
    elif min_price and max_price:
        products = controller.products.get_products_by_price_range(float(min_price), float(max_price))
    elif in_stock:
        products = controller.products.get_products_in_stock()
    else:
        products = controller.products.get_all()

    return jsonify([product.to_dict() for product in products]), 200

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
        product = controller.products.update(product_id, data)
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