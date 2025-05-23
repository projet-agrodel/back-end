from app import create_app, db # Assume que app é o diretório do seu pacote Flask
from app.models.user import User # Ajuste o caminho se User estiver em outro lugar

def check_alice():
    app_instance = create_app() # Cria a instância da aplicação
    
    # Não é estritamente necessário chamar db.init_app(app_instance) aqui
    # se create_app já o faz de forma que o contexto do app funcione para o db.
    # Se você tiver problemas de contexto, pode adicionar:
    # db.init_app(app_instance) 

    with app_instance.app_context(): # Entra no contexto da aplicação
        print("--- Verificando Usuário Alice ---")
        alice = User.query.filter_by(email="alice@email.com").first()
        
        if alice:
            print(f"Alice encontrada: ID={alice.id}, Nome={alice.name}, Senha (no DB)={alice.password}, Tipo={alice.type}")
            
            # Verificar o tipo explicitamente
            if hasattr(alice.type, 'value'): # Se for um Enum com .value
                tipo_valor = alice.type.value
            else: # Se for uma string direta
                tipo_valor = str(alice.type)

            if tipo_valor == 'admin':
                print("✅ Tipo de Alice é 'admin'. Correto!")
            else:
                print(f"⚠️ ATENÇÃO: Tipo de Alice é '{tipo_valor}', mas deveria ser 'admin'.")

            if alice.id == 1:
                print("✅ ID de Alice é 1. Correto para a configuração atual do token!")
            else:
                print(f"⚠️ ATENÇÃO: ID de Alice é {alice.id}. Você precisará usar este ID ({alice.id})")
                print(f"   na constante ADMIN_USER_ID_PARA_TOKEN em 'back-end/app/routes/admin_routes.py'")
                print(f"   em vez de 1.")
        else:
            print("❌ Usuário Alice (email='alice@email.com') não encontrado.")
            print("   Verifique se o script 'inserir_usuarios' está funcionando corretamente")
            print("   e se os dados foram commitados ao banco.")
        print("--- Fim da Verificação ---")

if __name__ == '__main__':
    check_alice()
