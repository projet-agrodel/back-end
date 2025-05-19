import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../instance/app.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:3000'
    # SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') # Remover SendGrid
    
    # Configurações do Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') # Ex: 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587) # Ex: 587 (TLS) ou 465 (SSL)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't'] # Usar TLS? (Gmail usa)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't'] # Usar SSL?
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # Seu email remetente
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # Senha do seu email (ou senha de app para Gmail)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'nao-responda@agrodel.com'