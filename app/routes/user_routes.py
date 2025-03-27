from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any

bp = Blueprint('users', __name__)
controller = MainController()

@bp.route('/users', methods=['POST'])
def create_user() -> tuple[Any, int]:
    try:
        data = request.get_json()
        user = controller.users.create_user(data)
        return jsonify({'message': 'Usuário criado com sucesso', 'id': user.id }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@bp.route('/users', methods=['GET'])
def get_users() -> tuple[Any, int]:
    query = request.args.get('query')
    user_type = request.args.get('type')

    if query:
        users = controller.users.search_users(query)
    elif user_type:
        users = controller.users.get_users_by_type(user_type)
    else:
        users = controller.users.get_all()

    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> tuple[Any, int]:
    user = controller.users.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        user = controller.users.update_user(user_id, data)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> tuple[Any, int]:
    try:
        if controller.users.delete(user_id):
            return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        return jsonify({'error': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400 