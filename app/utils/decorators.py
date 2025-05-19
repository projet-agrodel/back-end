from functools import wraps
<<<<<<< HEAD
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from flask import jsonify, request
=======
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from ..models.user import User, UserType
>>>>>>> dvd

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "admin":
            return jsonify(msg="Acesso restrito a administradores!"), 403
        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") not in ["user", "admin"]:
            return jsonify(msg="Acesso restrito a usuários registrados!"), 403
        return fn(*args, **kwargs)
    return wrapper

# Para funcionalidades que *apenas* usuários do tipo 'user' podem acessar (e não admins):
def specific_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("user_type") != "user":
            return jsonify(msg="Acesso restrito a usuários do tipo 'user'!"), 403
        return fn(*args, **kwargs)
    return wrapper

def admin_or_owner_required(resource_user_id_param="user_id"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
<<<<<<< HEAD
            claims = get_jwt()
            current_user_id_from_token = get_jwt_identity()
            
            requested_user_id = kwargs.get(resource_user_id_param)
            
            if requested_user_id is None and hasattr(request, 'view_args') and request.view_args:
                requested_user_id = request.view_args.get(resource_user_id_param)
            
            if requested_user_id is None:
                print(f"Erro no decorator admin_or_owner_required: Não foi possível encontrar o parâmetro '{resource_user_id_param}' na rota.")
                return jsonify(msg=f"Configuração de rota inválida: parâmetro '{resource_user_id_param}' não encontrado."), 500

            if claims.get("user_type") == "admin" or str(requested_user_id) == str(current_user_id_from_token):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Acesso negado. Requer permissão de administrador ou ser o proprietário do recurso."), 403
        return wrapper
    return decorator

# Nota: O decorator @jwt_required do flask_jwt_extended já garante que o usuário está logado.
# O @user_required acima é uma camada adicional se precisarmos diferenciar tipos específicos
# de usuários para certas rotas que não são exclusivamente de admin.
# Para rotas que apenas requerem um usuário logado (qualquer tipo), @jwt_required é o ideal. 
=======
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
>>>>>>> dvd
