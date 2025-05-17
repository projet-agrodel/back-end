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

@bp.route('/user/change-password', methods=['POST'])
@jwt_required()
def change_password() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')

        if not all([current_password, new_password, confirm_password]):
            return jsonify({'message': 'Todos os campos são obrigatórios.'}), 400

        if new_password != confirm_password:
            return jsonify({'message': 'A nova senha e a confirmação não coincidem.'}), 400

        # Lógica para verificar a senha atual e atualizar para a nova senha
        # Isso será movido para o controller
        success = controller.users.change_password(user_id, current_password, new_password)
        
        if success:
            return jsonify({'message': 'Senha alterada com sucesso.'}), 200
        else:
            # A mensagem de erro específica virá do controller
            return jsonify({'message': 'Não foi possível alterar a senha. Verifique sua senha atual.'}), 400
            
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        user = controller.users.get_by_id(user_id)
        if not user:
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar informações do perfil.'}), 500 