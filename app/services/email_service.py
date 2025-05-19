from flask import current_app
from flask_mail import Message # Importar Message do Flask-Mail
from ..extensions import mail # Importar a instância mail do Flask-Mail
import logging # Para logging

# Configurar um logger básico para o serviço de email
logger = logging.getLogger(__name__)

# Esta é uma função placeholder. Você precisará integrá-la com um serviço de email real.
# Exemplo: SendGrid, Flask-Mail com SMTP, etc.

def send_reset_password_email(to_email: str, username: str, token: str):
    """
    Envia um email de redefinição de senha para o usuário usando Flask-Mail.
    
    Args:
        to_email: O email do destinatário.
        username: O nome do usuário (para personalização do email).
        token: O token de redefinição de senha.
    """
    frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
    reset_url = f"{frontend_url}/auth/reset-password/{token}"
    
    subject = "Redefinição de Senha - AgroDel"
    # MAIL_DEFAULT_SENDER é usado automaticamente pelo Flask-Mail se configurado e não especificado aqui
    # from_email = current_app.config.get('MAIL_DEFAULT_SENDER') 

    # Verificar se as configurações essenciais do Flask-Mail estão presentes
    if not all([current_app.config.get('MAIL_SERVER'), 
                current_app.config.get('MAIL_USERNAME'), 
                current_app.config.get('MAIL_PASSWORD')]):
        logger.error("Configurações do Flask-Mail incompletas (MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD). O email não será enviado.")
        print("---- ERRO: Configurações do Flask-Mail incompletas. SIMULAÇÃO DE ENVIO DE EMAIL ----")
        print(f"Para: {to_email}")
        print(f"Assunto: {subject}")
        print(f"Link (simulado): {reset_url}")
        print("---- FIM DA SIMULAÇÃO ----")
        return

    body_html = f"""<p>Olá {username},</p>
<p>Você solicitou a redefinição da sua senha para sua conta na AgroDel.</p>
<p>Por favor, clique no link abaixo para criar uma nova senha:</p>
<p><a href=\"{reset_url}\">Redefinir Minha Senha</a></p>
<p>Se você não solicitou esta alteração, por favor, ignore este email.<br>
O link expirará em 1 hora.</p>
<p>Atenciosamente,<br>
Equipe AgroDel</p>
"""
    # Corpo em texto plano para clientes de email que não suportam HTML
    body_text = f"""Olá {username},

Você solicitou a redefinição da sua senha para sua conta na AgroDel.

Por favor, copie e cole o seguinte link no seu navegador para criar uma nova senha:
{reset_url}

Se você não solicitou esta alteração, por favor, ignore este email.
O link expirará em 1 hora.

Atenciosamente,
Equipe AgroDel
"""

    msg = Message(
        subject=subject,
        recipients=[to_email],
        # sender=from_email, # Opcional, MAIL_DEFAULT_SENDER é usado por padrão
        body=body_text, # Conteúdo em texto plano
        html=body_html  # Conteúdo em HTML
    )

    try:
        mail.send(msg)
        logger.info(f"Email de redefinição enviado para {to_email} via Flask-Mail.")
    except Exception as e:
        logger.error(f"Exceção ao enviar email de redefinição para {to_email} via Flask-Mail: {e}")
        print(f"---- EXCEÇÃO ao enviar via Flask-Mail: {e}. SIMULAÇÃO DE ENVIO DE EMAIL ----")
        print(f"Para: {to_email}")
        print(f"Assunto: {subject}")
        print(f"Link (simulado): {reset_url}")
        print("---- FIM DA SIMULAÇÃO ----")
    pass 