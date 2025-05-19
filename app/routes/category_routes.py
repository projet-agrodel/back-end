from flask import Blueprint, request, jsonify
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('categories', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/categories', methods=['POST'])
@admin_required
def create_category() -> tuple[Any, int]:
    try:
        data = request.get_json()
        category = controller.categories.create_category(data['name'])
        return jsonify(category.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/categories', methods=['GET'])
def get_categories() -> tuple[Any, int]:
    query = request.args.get('query')
    if query:
        categories = controller.categories.search_by_name(query)
    else:
        categories = controller.categories.get_all()
    return jsonify([category.to_dict() for category in categories]), 200

@bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id: int) -> tuple[Any, int]:
    category = controller.categories.get_by_id(category_id)
    if not category:
        return jsonify({'error': 'Categoria não encontrada'}), 404
    return jsonify(category.to_dict()), 200

@bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        category = controller.categories.update(category_id, data)
        if not category:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id: int) -> tuple[Any, int]:
    try:
        if controller.categories.delete(category_id):
            return jsonify({'message': 'Categoria deletada com sucesso'}), 200
        return jsonify({'error': 'Categoria não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400 