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
    from .routes import user_routes, product_routes

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(product_routes.bp)

    return app 