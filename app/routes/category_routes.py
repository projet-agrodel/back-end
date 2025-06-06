from flask import Blueprint, request, jsonify
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('categories', __name__, url_prefix='/categories')

controller = MainController()

@bp.route('', methods=['GET'])
def get_categories():
    try:
        categories = controller.categories.get_all()
        return jsonify({ 'categories': [category.to_dict() for category in categories] })
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

@bp.route('', methods=['POST'])
def create_category():
    try:
     data = request.get_json()
     category = controller.categories.create_category(data.get('name'))

     return jsonify({ 'category': category.to_dict() })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = controller.categories.get_by_id(category_id)
        return jsonify({ 'category': category.to_dict() })
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        category = controller.categories.update(category_id)
        return jsonify({ 'category': category.to_dict() })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
       controller.categories.delete(category_id) 
       return jsonify({'message': 'Deletada com sucesso' }), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500