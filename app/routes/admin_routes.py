from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
# from app.extensions import bcrypt # Descomente se for usar hash de senha do DB
# from ..models.user import User # Se precisar buscar o usuário do DB

# Credenciais para o admin "Alice" (do script inserir_usuarios)
ADMIN_EMAIL = "alice@email.com"
ADMIN_PASSWORD = "senha123" # Senha em texto plano, como no script inserir_usuarios
ADMIN_USER_ID_PARA_TOKEN = 3 # ATUALIZADO para o ID real de Alice (3)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # No frontend, o campo de "username" para login pode enviar um email
    identifier = data.get('username', None) # Pode ser username ou email
    password = data.get('password', None)

    if not identifier or not password:
        return jsonify({"msg": "Missing identifier (username/email) or password"}), 400

    # Validação de credenciais (usando dados de "Alice")
    # Em um cenário real, você buscaria o usuário pelo email/username,
    # verificaria a senha (hasheada) e então pegaria o ID do usuário.
    if identifier == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        # IMPORTANTE: Converter o ID para string antes de usar como identity
        # Flask-JWT-Extended espera que identity seja uma string por padrão
        admin_id_to_use_in_token = str(ADMIN_USER_ID_PARA_TOKEN)  # Convertido para string
        
        access_token = create_access_token(identity=admin_id_to_use_in_token, additional_claims={"is_administrator": True})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad identifier or password"}), 401

# Outras rotas de admin podem ser adicionadas aqui no futuro.
# Exemplo:
# @admin_bp.route('/products', methods=['GET'])
# @jwt_required() # Isso protegeria a rota
# def get_admin_products():
#     # Lógica para buscar produtos para admin
#     current_user = get_jwt_identity()
#     claims = get_jwt()
#     if not claims.get("is_administrator"):
#         return jsonify(msg="Administration rights required"), 403
#     return jsonify(products_list_for_admin), 200 