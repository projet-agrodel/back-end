from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
# from app.extensions import bcrypt # Descomente se for usar hash de senha do DB
# from ..models.user import User # Se precisar buscar o usuário do DB

ADMIN_EMAIL = "alice@email.com"
ADMIN_PASSWORD = "senha123"
ADMIN_USER_ID_PARA_TOKEN = 3 

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

    if identifier == ADMIN_EMAIL and password == ADMIN_PASSWORD:

        admin_id_to_use_in_token = str(ADMIN_USER_ID_PARA_TOKEN) 
        
        access_token = create_access_token(identity=admin_id_to_use_in_token, additional_claims={"is_administrator": True})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad identifier or password"}), 401