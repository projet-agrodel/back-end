from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..controllers.base.main_controller import MainController
from ..extensions import bcrypt
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')
controller = MainController()

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"}), 400

        # Buscar usuário pelo email usando o controller
        user = controller.users.get_by_email(email)

        # Verificar se usuário existe e a senha está correta
        if user and bcrypt.check_password_hash(user.password, password):
            # Senha correta, gerar token JWT
            # A identidade do token pode ser o ID do usuário ou o email
            # O tempo de expiração pode ser configurado globalmente ou aqui
            access_token = create_access_token(identity=user.id) # Usando ID como identidade
            return jsonify(access_token=access_token), 200
        else:
            # Usuário não encontrado ou senha incorreta
            return jsonify({"message": "Credenciais inválidas"}), 401

    except Exception as e:
        # Logar o erro real pode ser útil aqui
        print(f"Erro no login: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500

# Opcional: Adicionar rota de refresh token, logout, etc. aqui no futuro 