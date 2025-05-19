from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from ..models.user import User, UserType

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            try:
                user_id_as_int = int(current_user_id)
            except ValueError:
                return jsonify({'error': 'Identidade do usuário inválida no token.'}), 401

            current_user = User.query.get(user_id_as_int)
            
            if not current_user:
                return jsonify({'error': 'Usuário do token não encontrado.'}), 401

            if current_user.type != UserType.admin:
                return jsonify({'error': 'Acesso negado. Requer privilégios de administrador.'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper 