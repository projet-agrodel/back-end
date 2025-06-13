# Importar db do novo local
from ..extensions import db, bcrypt
from ..models.user import User
from ..models.product import Product
from ..models.category import Category
from ..models.payment import Payment
from decimal import Decimal

def criar_tabelas(app):
    with app.app_context():
        print("Verificando/Criando tabelas...")
        db.create_all()
        print("✅ Tabelas verificadas/criadas.")

# Função para deletar as tabelas
def deletar_tabelas(app):
    with app.app_context():
        db.drop_all()
        print("❌ Tabelas deletadas com sucesso!")

# Função para inserir usuários fixos
def inserir_usuarios(app):
    with app.app_context():
        if User.query.filter_by(email="alice@email.com").first() is None:
            print("Inserindo usuários fixos...")
            usuarios = [
                User(name="Alice", email="lucas@gmail.com.br", password=bcrypt.generate_password_hash("C123456789").decode('utf-8'), phone="11999999999", type='admin'),
                User(name="Bob", email="bob@email.com", password=bcrypt.generate_password_hash("senha456").decode('utf-8'), phone="11888888888", type='admin'),
                User(name="Charlie", email="charlie@email.com", password=bcrypt.generate_password_hash("senha789").decode('utf-8'), phone="11777777777", type='admin'),
                User(name="Doge", email="davidjmacedo@hotmail.com", password=bcrypt.generate_password_hash("Senha@123").decode('utf-8'), phone="11777777777", type='admin')
            ]
            try:
                db.session.add_all(usuarios)
                db.session.commit()
                print("✅ Usuários inseridos com sucesso!")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao inserir usuários: {e}")
        else:
            print("Usuários fixos já existem.")

# Função para inserir clientes fictícios
def inserir_clientes_ficticios(app):
    with app.app_context():
        print("Verificando se clientes fictícios precisam ser inseridos...")
        clientes_ficticios_data = [
            {"name": "Fernanda Lima", "email": "fernanda.lima@example.com", "password": "Password123", "phone": "21987654321", "type": "user"},
            {"name": "Ricardo Souza", "email": "ricardo.souza@example.com", "password": "Password123", "phone": "31912345678", "type": "user"},
            {"name": "Camila Oliveira", "email": "camila.oliveira@example.com", "password": "Password123", "phone": "41988887777", "type": "user"},
            {"name": "Lucas Martins", "email": "lucas.martins@example.com", "password": "Password123", "phone": "51977778888", "type": "user"},
            {"name": "Juliana Alves", "email": "juliana.alves@example.com", "password": "Password123", "phone": "61966665555", "type": "user"},
            {"name": "Gabriel Pereira", "email": "gabriel.pereira@example.com", "password": "Password123", "phone": "71955556666", "type": "user"},
            {"name": "Beatriz Costa", "email": "beatriz.costa@example.com", "password": "Password123", "phone": "81944443333", "type": "user"},
            {"name": "Matheus Ferreira", "email": "matheus.ferreira@example.com", "password": "Password123", "phone": "91933334444", "type": "user"},
            {"name": "Larissa Rodrigues", "email": "larissa.rodrigues@example.com", "password": "Password123", "phone": "11922221111", "type": "user"},
            {"name": "Thiago Almeida", "email": "thiago.almeida@example.com", "password": "Password123", "phone": "22911112222", "type": "user"}
        ]

        clientes_para_adicionar = []
        for cliente_data in clientes_ficticios_data:
            if User.query.filter_by(email=cliente_data["email"]).first() is None:
                hashed_password = bcrypt.generate_password_hash(cliente_data["password"]).decode('utf-8')
                clientes_para_adicionar.append(
                    User(
                        name=cliente_data["name"],
                        email=cliente_data["email"],
                        password=hashed_password,
                        phone=cliente_data["phone"],
                        type=cliente_data["type"]
                    )
                )
        
        if clientes_para_adicionar:
            try:
                db.session.add_all(clientes_para_adicionar)
                db.session.commit()
                print(f"✅ {len(clientes_para_adicionar)} clientes fictícios inseridos com sucesso!")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao inserir clientes fictícios: {e}")
        else:
            print("Nenhum novo cliente fictício para adicionar ou já existem.")

# Função para inserir categorias
def inserir_categorias(app):
    """Insere as categorias padrão do Agrodel se não existirem."""
    with app.app_context():
        if Category.query.first() is None:
            print("Populando categorias Agrodel...")
            categories_to_add = [
                Category(name='Fertilizantes'),
                Category(name='Sementes'),
                Category(name='Ferramentas'),
                Category(name='Defensivos'),
                Category(name='Substratos')
            ]
            try:
                db.session.add_all(categories_to_add)
                db.session.commit()
                print(f"✅ {len(categories_to_add)} categorias Agrodel adicionadas.")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao popular categorias Agrodel: {e}")
        else:
            print("Categorias Agrodel já existem.")

# Função para inserir produtos
def inserir_produtos(app):
    """Insere os 12 produtos padrão do Agrodel se não existirem."""
    with app.app_context():
        if Product.query.first() is None:
            print("Populando produtos Agrodel...")
            categories_db = {cat.name: cat for cat in Category.query.all()}
            if not categories_db:
                print("⚠️ Erro: Nenhuma categoria encontrada no banco. Produtos não podem ser associados.")
                return
                
            products_data = [
                { 'name': 'Fertilizante Orgânico', 'price': 45.99, 'description': 'Fertilizante orgânico de alta qualidade para todos os tipos de plantas.', 'stock': 50, 'category_name': 'Fertilizantes' },
                { 'name': 'Semente de Alface', 'price': 12.50, 'description': 'Sementes de alface crespa de alta germinação, pacote com 100 unidades.', 'stock': 120, 'category_name': 'Sementes' },
                { 'name': 'Regador Manual 5L', 'price': 29.90, 'description': 'Regador manual com capacidade para 5 litros, ideal para jardins e hortas.', 'stock': 35, 'category_name': 'Ferramentas' },
                { 'name': 'Herbicida Natural', 'price': 38.75, 'description': 'Herbicida natural à base de extratos vegetais, não agride o meio ambiente.', 'stock': 45, 'category_name': 'Defensivos' },
                { 'name': 'Substrato para Plantas', 'price': 18.99, 'description': 'Substrato de alta qualidade para vasos e jardins, embalagem de 5kg.', 'stock': 80, 'category_name': 'Substratos' },
                { 'name': 'Kit Ferramentas de Jardim', 'price': 89.90, 'description': 'Kit completo com 5 ferramentas essenciais para jardinagem.', 'stock': 25, 'category_name': 'Ferramentas' },
                { 'name': 'Fertilizante NPK 10-10-10', 'price': 52.80, 'description': 'Fertilizante mineral balanceado para desenvolvimento completo das plantas.', 'stock': 65, 'category_name': 'Fertilizantes' },
                { 'name': 'Sementes de Tomate Cereja', 'price': 15.99, 'description': 'Sementes selecionadas de tomate cereja, alta produtividade.', 'stock': 90, 'category_name': 'Sementes' },
                { 'name': 'Pulverizador 2L', 'price': 35.50, 'description': 'Pulverizador manual com capacidade de 2 litros para aplicação de defensivos.', 'stock': 40, 'category_name': 'Ferramentas' },
                { 'name': 'Inseticida Biológico', 'price': 42.99, 'description': 'Inseticida à base de Bacillus thuringiensis, controle biológico de pragas.', 'stock': 30, 'category_name': 'Defensivos' },
                { 'name': 'Substrato para Cactos', 'price': 22.50, 'description': 'Substrato especial para cactos e suculentas, drenagem ideal.', 'stock': 55, 'category_name': 'Substratos' },
                { 'name': 'Pá de Jardinagem', 'price': 18.75, 'description': 'Pá de jardinagem com cabo ergonômico, ideal para transplantes.', 'stock': 60, 'category_name': 'Ferramentas' }
            ]
            
            new_products = []
            for prod_data in products_data:
                category = categories_db.get(prod_data['category_name'])
                if category:
                    new_products.append(Product(
                        name=prod_data['name'],
                        description=prod_data['description'],
                        price=Decimal(str(prod_data['price'])), 
                        stock=prod_data['stock'],
                        category_id=category.id
                    ))
                else:
                    print(f"Aviso: Categoria '{prod_data['category_name']}' não encontrada para o produto '{prod_data['name']}'")
            
            try:
                db.session.add_all(new_products)
                db.session.commit()
                print(f"✅ {len(new_products)} produtos Agrodel adicionados.")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao popular produtos Agrodel: {e}")
        else:
             print("Produtos Agrodel já existem.")

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

def inserir_pedidos_ficticios(app):
    """Insere pedidos fictícios para teste no sistema."""
    from app.models.order import Order, OrderItem, OrderStatus
    from app.models.user import User
    from app.models.product import Product
    from datetime import datetime, timedelta
    import random

    with app.app_context():
        if Order.query.first() is None:
            print("Populando pedidos fictícios...")
            
            # Obtém usuários e produtos existentes
            users = User.query.all()
            products = Product.query.all()
            
            if not users or not products:
                print("⚠️ Erro: Necessário ter usuários e produtos cadastrados primeiro")
                return
                
            # Status possíveis para os pedidos
            status_list = list(OrderStatus)
            
            # Cria 20 pedidos fictícios
            orders_to_add = []
            for i in range(20):
                # Seleciona um usuário aleatório
                user = random.choice(users)
                
                # Define uma data aleatória nos últimos 30 dias
                random_days = random.randint(0, 30)
                order_date = datetime.utcnow() - timedelta(days=random_days)
                
                # Cria o pedido
                order = Order(
                    user_id=user.id,
                    description=f"Pedido de teste #{i+1}".encode(),
                    status=random.choice(status_list),
                    created_at=order_date,
                    updated_at=order_date,
                    amount=Decimal('0.0')  # Será calculado com base nos itens
                )
                
                # Adiciona 1-5 itens aleatórios ao pedido
                total_amount = Decimal('0.0')
                num_items = random.randint(1, 5)
                selected_products = random.sample(products, num_items)
                
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    item_amount = product.price * Decimal(str(quantity))
                    total_amount += item_amount
                    
                    order_item = OrderItem(
                        pedido_id=order.id,
                        produto_id=product.id,
                        quantity=quantity,
                        price=item_amount
                    )
                    order.items.append(order_item)
                
                order.payments.append(Payment(
                    amount=total_amount,
                    payment_method='PIX',
                    pedido_id=order.id,
                    transaction_id='34534254543345345'
                ))

                order.amount = total_amount
                orders_to_add.append(order)
            
            try:
                db.session.add_all(orders_to_add)
                db.session.commit()
                print(f"✅ {len(orders_to_add)} pedidos fictícios adicionados com sucesso!")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao inserir pedidos fictícios: {e}")
        else:
            print("Pedidos já existem no banco de dados.")
