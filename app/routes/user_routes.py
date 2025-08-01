from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any
import re

bp = Blueprint('users', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/users', methods=['POST'])
def create_user() -> tuple[Any, int]:
    try:
        data = request.get_json()
        password = data.get('password') # Obter a senha para validação

        # Validação de campos básicos (exemplo, adicione outros se necessário)
        if not data.get('name') or not data.get('email') or not password:
            return jsonify({'message': 'Nome, email e senha são obrigatórios.'}), 400

        # Validação de complexidade da senha no backend
        if len(password) < 8:
            return jsonify({'message': 'A senha deve ter pelo menos 8 caracteres.'}), 400
        if not re.search(r"[A-Z]", password):
            return jsonify({'message': 'A senha deve conter pelo menos uma letra maiúscula.'}), 400
        if not re.search(r"[0-9]", password):
            return jsonify({'message': 'A senha deve conter pelo menos um número.'}), 400

        user = controller.users.create_user(data)
        return jsonify({
            'message': 'Usuário criado com sucesso', 
            'user': {'id': user.id, 'name': user.name, 'email': user.email, 'type': user.type.value }
        }), 201
    except ValueError as e: # Capturar ValueError para emails duplicados, etc.
        return jsonify({'message': str(e)}), 409 # 409 Conflict pode ser mais apropriado
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

        # Validação de complexidade da nova senha no backend
        if len(new_password) < 8:
            return jsonify({'message': 'A nova senha deve ter pelo menos 8 caracteres.'}), 400
        if not re.search(r"[A-Z]", new_password):
            return jsonify({'message': 'A nova senha deve conter pelo menos uma letra maiúscula.'}), 400
        if not re.search(r"[0-9]", new_password):
            return jsonify({'message': 'A nova senha deve conter pelo menos um número.'}), 400

        success = controller.users.change_password(user_id, current_password, new_password)
        
        if success:
            return jsonify({'message': 'Senha alterada com sucesso.'}), 200
        else:
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

@bp.route('/users/<int:user_id>/status', methods=['PATCH'])
@jwt_required()
def update_user_status(user_id: int):
    # Verificação manual de admin
    claims = get_jwt()
    if not claims.get("is_administrator"):
        return jsonify(msg="Acesso restrito para administradores!"), 403

    data = request.get_json()
    status = data.get('status')

    if not status:
        return jsonify({'message': 'O status é obrigatório.'}), 400

    try:
        user = controller.users.update_user_status(user_id, status)
        if not user:
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        
        return jsonify({
            'message': 'Status do usuário atualizado com sucesso.',
            'user': user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Ocorreu um erro ao atualizar o status do usuário.'}), 500

@bp.route('/user/notification-settings', methods=['PUT'])
@jwt_required()
def update_notification_settings():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if 'notify_new_order' not in data and 'notify_stock_alert' not in data:
            return jsonify({'message': 'Pelo menos uma configuração de notificação deve ser fornecida.'}), 400

        user = controller.users.update_notification_settings(user_id, data)

        if not user:
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        
        return jsonify({
            'message': 'Configurações de notificação atualizadas com sucesso.',
            'settings': {
                'notify_new_order': user.notify_new_order,
                'notify_stock_alert': user.notify_stock_alert
            }
        }), 200
    except Exception as e:
        return jsonify({'message': 'Ocorreu um erro ao atualizar as configurações de notificação.'}), 500 