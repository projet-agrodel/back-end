from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..controllers.base.main_controller import MainController
from ..extensions import bcrypt, db
from datetime import datetime, timedelta
import secrets
from ..services.email_service import send_reset_password_email

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
            # A identidade do token deve ser uma string.
            # O tempo de expiração pode ser configurado globalmente ou aqui
            access_token = create_access_token(identity=str(user.id)) # Convertendo user.id para string
            user_data_for_response = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            return jsonify(access_token=access_token, user=user_data_for_response), 200
        else:
            # Usuário não encontrado ou senha incorreta
            return jsonify({"message": "Credenciais inválidas"}), 401

    except Exception as e:
        # Logar o erro real pode ser útil aqui
        print(f"Erro no login: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500

# Opcional: Adicionar rota de refresh token, logout, etc. aqui no futuro 

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email é obrigatório"}), 400

    user = controller.users.get_by_email(email)

    if user:
        # Gerar token seguro
        token = secrets.token_urlsafe(32)
        # Definir tempo de expiração (e.g., 1 hora)
        expiration_time = datetime.utcnow() + timedelta(hours=1)

        user.reset_password_token = token
        user.reset_password_expiration = expiration_time
        
        try:
            db.session.commit()
            # Lógica de envio de email aqui
            send_reset_password_email(to_email=user.email, username=user.name, token=token)
            print(f"Token de redefinição para {user.email}: {token}") # Log para desenvolvimento
            return jsonify({"message": "Se o email estiver cadastrado, um link de redefinição foi enviado."}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar token de redefinição: {e}")
            return jsonify({"message": "Erro ao processar a solicitação."}), 500
    else:
        # Mesmo que o usuário não exista, retornar uma mensagem genérica por segurança
        print(f"Tentativa de redefinição para email não encontrado: {email}") # Log para desenvolvimento
        return jsonify({"message": "Se o email estiver cadastrado, um link de redefinição foi enviado."}), 200

@bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not new_password or not confirm_password:
        return jsonify({"message": "Nova senha e confirmação são obrigatórias"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "As senhas não coincidem"}), 400

    # Buscar usuário pelo token
    user = controller.users.get_by_reset_token(token) # Assume que você adicionará este método ao controller

    if not user:
        return jsonify({"message": "Token inválido ou expirado."}), 400
        
    # Verificar se o token não expirou (redundante se get_by_reset_token já verificar, mas bom para clareza)
    if user.reset_password_expiration < datetime.utcnow():
        # Invalidar token se expirado e ainda não tratado pelo get_by_reset_token
        user.reset_password_token = None
        user.reset_password_expiration = None
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao limpar token expirado: {e}")
            # Não precisa notificar o usuário sobre este erro interno especificamente
        return jsonify({"message": "Token expirado."}), 400

    # Atualizar a senha
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    
    # Invalidar o token após o uso bem-sucedido
    user.reset_password_token = None
    user.reset_password_expiration = None

    try:
        db.session.commit()
        return jsonify({"message": "Senha redefinida com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao redefinir senha: {e}")
        return jsonify({"message": "Erro ao redefinir a senha."}), 500 