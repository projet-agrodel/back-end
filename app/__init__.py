from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_bcrypt import Bcrypt
from .config import Config
from app.controllers.base.main_controller import MainController
from app.services.encryption_service import EncryptionService

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

main_controller = MainController()
encryption_service = EncryptionService()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Middleware para verificar autenticação e autorização
    @app.before_request
    def require_authentication():
        try:
            verify_jwt_in_request()
            current_user = main_controller.users.get_user_by_id(get_jwt_identity())
            if current_user.type != 'admin':
                return jsonify({'error': 'Acesso negado'}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 401

    # Importa e registra as blueprints
    from .routes import user_routes, product_routes

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(product_routes.bp)

    return app 