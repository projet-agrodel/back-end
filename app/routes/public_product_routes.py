from flask import Blueprint, request, jsonify
from app.controllers.base.main_controller import MainController
from typing import Any

# Usar um nome de blueprint diferente para evitar conflitos
bp = Blueprint('public_products', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/products', methods=['GET'])
def get_public_products() -> tuple[Any, int]:
    query = request.args.get('q') 
    category_id = request.args.get('category_id', type=int) 
    min_price_str = request.args.get('minPrice')
    max_price_str = request.args.get('maxPrice')
    sort = request.args.get('sort')

    min_price = None
    if min_price_str:
        try:
            min_price = float(min_price_str)
        except ValueError:
            pass 
            
    max_price = None
    if max_price_str:
        try:
            max_price = float(max_price_str)
        except ValueError:
            pass

    try:
        # Supondo que controller.products.get_all() pode ser usado ou adaptado
        # para busca pública, ou um novo método como get_all_public é criado.
        # Por simplicidade, vamos assumir que get_all pode receber mais filtros.
        products = controller.products.get_all(
            query=query,
            category_id=category_id, # Adicionar filtro de categoria ao controller.products.get_all
            min_price=min_price, 
            max_price=max_price, 
            sort=sort,
            status='Ativo' # Garantir que apenas produtos ativos sejam listados publicamente
        )
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        print(f"Erro ao buscar produtos públicos: {e}")
        return jsonify({'error': "Erro interno ao buscar produtos."}), 500

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_public_product_details(product_id: int) -> tuple[Any, int]:
    product = controller.products.get_by_id(product_id)
    if not product or product.status != 'Ativo': # Apenas produtos ativos
        return jsonify({'error': 'Produto não encontrado ou indisponível'}), 404
    return jsonify(product.to_dict()), 200 

@bp.route('/products/<int:product_id>/availability', methods=['GET'])
def check_product_availability(product_id: int) -> tuple[Any, int]:
    """
    Verifica a disponibilidade de estoque de um produto.
    Retorna o estoque atual e status de disponibilidade.
    """
    try:
        # Obter a quantidade solicitada do query params (opcional)
        quantity = request.args.get('quantity', default=1, type=int)
        
        # Usar o método melhorado do controller
        result = controller.products.check_stock_availability(product_id, quantity)
        
        if 'error' in result and result['error'] == 'Produto não encontrado':
            return jsonify(result), 404
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao verificar disponibilidade do produto {product_id}: {e}")
        return jsonify({
            'error': "Erro interno ao verificar disponibilidade do produto.",
            'available': False,
            'stock': 0,
            'requested': quantity if 'quantity' in locals() else 1
        }), 500 