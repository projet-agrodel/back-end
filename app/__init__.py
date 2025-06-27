import os # Importar os
from flask import Flask
from flask_cors import CORS # Manter a importação
from .config import Config
# Importar instâncias das extensões
from .extensions import db, bcrypt, jwt, mail
from flask_migrate import Migrate
from .services.database_manager import criar_tabelas, inserir_categorias,inserir_produtos, inserir_usuarios, inserir_clientes_ficticios
from flask_jwt_extended import JWTManager

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False) # Garantir que instance folder não interfira
    app.config.from_object(config_class)

    # Inicializar extensões ANTES de registrar blueprints
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    # Configurar CORS o mais cedo possível
    CORS(app, origins="*", supports_credentials=True) # Temporariamente mais permissivo para depuração

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
    app.register_blueprint(order_routes.order_bp)
    app.register_blueprint(payment_routes.bp)    
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(card_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(admin_analytics_routes.bp)

    with app.app_context():
        criar_tabelas(app)
        inserir_categorias(app)
        inserir_produtos(app)
        inserir_usuarios(app)
        inserir_clientes_ficticios(app)

    return app
