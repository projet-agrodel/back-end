from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)

    # Importa e registra as blueprints
    from .routes import (
        user_routes, product_routes, ticket_routes,
        category_routes, order_routes, payment_routes,
        cart_routes, card_routes
    )

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(ticket_routes.bp)
    app.register_blueprint(category_routes.bp)
    app.register_blueprint(order_routes.bp)
    app.register_blueprint(payment_routes.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(card_routes.bp)

    return app 