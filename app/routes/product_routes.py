from flask import Blueprint, request, jsonify
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('admin_products', __name__, url_prefix='/admin')
controller = MainController()

@bp.route('/products', methods=['POST'])
@admin_required()
def create_product() -> tuple[Any, int]:
    try:
        data = request.get_json()
        product = controller.products.create_product(data)
        return jsonify(product.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/list', methods=['GET'])
@admin_required()
def admin_get_products() -> tuple[Any, int]:
    query = request.args.get('query')
    min_price_str = request.args.get('min_price')
    max_price_str = request.args.get('max_price')
    sort = request.args.get('sort')
    status_filter = request.args.get('status_filter')
    
    print(f"Recebendo solicitação de produtos para admin. Status filter: {status_filter}")

    min_price = None
    if min_price_str:
        try:
            min_price = float(min_price_str)
        except ValueError:
            return jsonify({'error': "Parâmetro 'min_price' inválido."}), 400
            
    max_price = None
    if max_price_str:
        try:
            max_price = float(max_price_str)
        except ValueError:
            return jsonify({'error': "Parâmetro 'max_price' inválido."}), 400

    try:
        products = controller.products.get_all(
            query=query, 
            min_price=min_price, 
            max_price=max_price, 
            sort=sort, 
            status=status_filter,
            for_admin=True
        )
        print(f"Produtos encontrados: {len(products)}, incluindo status: {[p.status for p in products[:5]]}...")
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        print(f"Erro ao buscar produtos para admin: {e}")
        return jsonify({'error': "Erro interno ao buscar produtos para admin."}), 500

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int) -> tuple[Any, int]:
    product = controller.products.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    if product.status != 'Ativo':
        return jsonify({'error': 'Produto não disponível'}), 404
    
    return jsonify(product.to_dict()), 200

@bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required()
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
@admin_required()
def update_stock(product_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({'error': "O campo 'quantity' é obrigatório."}), 400
        
        product = controller.products.update_stock(product_id, quantity)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required()
def delete_product(product_id: int) -> tuple[Any, int]:
    try:
        if controller.products.delete(product_id):
            return jsonify({'message': 'Produto deletado com sucesso'}), 200
        return jsonify({'error': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400 