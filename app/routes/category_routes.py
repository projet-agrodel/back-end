from flask import Blueprint, request, jsonify
from app.controllers.category_controller import CategoryController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('', methods=['GET'])
def get_categories():
    return CategoryController.get_all_categories()

@bp.route('', methods=['POST'])
def create_category():
    return CategoryController.create_category()

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return CategoryController.get_category_by_id(category_id)

@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    return CategoryController.update_category(category_id)

@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    return CategoryController.delete_category(category_id) 