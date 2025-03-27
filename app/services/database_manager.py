from app import db
from app.models.user import User
from app.models.product import Product

def criar_tabelas(app):
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")

# Função para deletar as tabelas
def deletar_tabelas(app):
    with app.app_context():
        db.drop_all()
        print("❌ Tabelas deletadas com sucesso!")

# Função para inserir usuários fixos
def inserir_usuarios(app):
    with app.app_context():
        usuarios = [
            User(name="Alice", email="alice@email.com", password="senha123", phone="11999999999", salt='42243234234', type='admin'),
            User(name="Bob", email="bob@email.com", password="senha456", phone="11888888888", salt='42243234234', type='admin'),
            User(name="Charlie", email="charlie@email.com", password="senha789", phone="11777777777", salt='42243234234', type='admin'),
        ]
        db.session.add_all(usuarios)
        db.session.commit()
        print("✅ Usuários inseridos com sucesso!")

# Função para inserir produtos fixos
def inserir_produtos(app):
    with app.app_context():
        produtos = [
            Product(name="Teclado Mecânico", description="Teclado mecânico RGB", price=299.99, stock=50),
            Product(name="Mouse Gamer", description="Mouse com sensor óptico de alta precisão", price=199.99, stock=30),
            Product(name="Monitor 144Hz", description="Monitor Full HD 144Hz", price=1299.99, stock=15),
        ]
        db.session.add_all(produtos)
        db.session.commit()
        print("✅ Produtos inseridos com sucesso!")

# Função para listar usuários
def listar_usuarios(app):
    with app.app_context():
        usuarios = User.query.all()
        if usuarios:
            print("\n📌 Lista de Usuários:")
            for usuario in usuarios:
                print(f"ID: {usuario.id} | Nome: {usuario.name} | Email: {usuario.email} | Telefone: {usuario.phone}")
        else:
            print("⚠️ Nenhum usuário encontrado.")

# Função para listar produtos
def listar_produtos(app):
    with app.app_context():
        produtos = Product.query.all()
        if produtos:
            print("\n📌 Lista de Produtos:")
            for produto in produtos:
                print(f"ID: {produto.id} | Nome: {produto.name} | Preço: R${produto.price} | Estoque: {produto.stock}")
        else:
            print("⚠️ Nenhum produto encontrado.")
