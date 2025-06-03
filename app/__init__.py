import os # Importar os
from flask import Flask
from flask_cors import CORS # Manter a importação
from .config import Config
# Importar instâncias das extensões
from .extensions import db, bcrypt, jwt, mail
from flask_migrate import Migrate
from .services.database_manager import criar_tabelas, inserir_categorias, inserir_produtos, inserir_usuarios
# from flask_jwt_extended import JWTManager # JWTManager já está em extensions.jwt

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False) # Garantir que instance folder não interfira
    app.config.from_object(config_class)

    # Calcular e definir caminho absoluto para o DB, sobrescrevendo .env se necessário
    # app.root_path aponta para o diretório 'app', então subimos um nível
    backend_dir = os.path.dirname(app.root_path)
    db_path = os.path.join(backend_dir, 'test.db')
    db_uri = f'sqlite:///{db_path}'
    print(f"[INFO] Usando URI do Banco de Dados: {db_uri}") # Log para confirmação
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config.pop('DATABASE_URL', None)

    # Inicializar extensões ANTES de registrar blueprints
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    from .routes import (
        user_routes, product_routes, ticket_routes,
        category_routes, order_routes, payment_routes,
        cart_routes, card_routes, auth_routes,
        admin_routes, public_product_routes,
        admin_analytics_routes
    )

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(public_product_routes.bp)
    app.register_blueprint(ticket_routes.bp)
    app.register_blueprint(category_routes.bp)
    app.register_blueprint(order_routes.bp)
    app.register_blueprint(payment_routes.bp)    
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(card_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(admin_analytics_routes.bp)

    # Configurar CORS DEPOIS de registrar todos os blueprints
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    with app.app_context():
        criar_tabelas(app)
        inserir_categorias(app)
        inserir_produtos(app)
        inserir_usuarios(app)

    return app 