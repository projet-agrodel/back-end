from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import uuid

# Mock de dados de pedidos (similar ao que você tem no frontend)
# Adicionando mais detalhes e variedade aos mocks
MOCK_ORDERS_DATA = [
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00001",
        "customer": {"id": "cust1", "name": "Carlos Silva", "email": "carlos.silva@example.com", "phone": "11999990001"},
        "orderDate": (datetime.now() - timedelta(days=2)).isoformat() + "Z",
        "totalAmount": 250.75, "status": "Entregue", "itemCount": 9,
        "shippingAddress": {"street": "Rua das Palmeiras, 123", "city": "São Paulo", "zipCode": "01000-000", "country": "Brasil"},
        "paymentMethod": "Cartão de Crédito", "trackingNumber": "BR123456789SP",
        "items": [
            {"id": "item1", "productId": "prodA", "productName": "Produto Alpha", "quantity": 1, "unitPrice": 100, "totalPrice": 100, "imageUrl": "https://via.placeholder.com/100x100/FFA07A/000000?text=Alpha"},
            {"id": "item2", "productId": "prodB", "productName": "Produto Beta", "quantity": 1, "unitPrice": 150.75, "totalPrice": 150.75, "imageUrl": "https://via.placeholder.com/100x100/ADD8E6/000000?text=Beta"},
        ]
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00002",
        "customer": {"id": "cust2", "name": "Ana Pereira", "email": "ana.p@example.com", "phone": "21987654321"},
        "orderDate": (datetime.now() - timedelta(days=1)).isoformat() + "Z",
        "totalAmount": 120.00, "status": "Enviado", "itemCount": 1,
        "shippingAddress": {"street": "Av. Principal, 456", "city": "Rio de Janeiro", "zipCode": "20000-000", "country": "Brasil"},
        "paymentMethod": "PIX", "trackingNumber": "BR987654321RJ",
        "items": [
            {"id": "item3", "productId": "prodC", "productName": "Produto Charlie", "quantity": 1, "unitPrice": 120, "totalPrice": 120, "imageUrl": "https://via.placeholder.com/100x100/90EE90/000000?text=Charlie"},
        ]
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00003",
        "customer": {"id": "cust3", "name": "Maria Oliveira", "email": "maria.oliveira@example.com"},
        "orderDate": datetime.now().isoformat() + "Z",
        "totalAmount": 85.50, "status": "Processando", "itemCount": 2,
        "shippingAddress": {"street": "Rua Teste, 100", "city": "Belo Horizonte", "zipCode": "30000-000", "country": "Brasil"},
        "paymentMethod": "Boleto",
        "items": [
            {"id": "item4", "productId": "prodD", "productName": "Produto Delta", "quantity": 1, "unitPrice": 50, "totalPrice": 50},
            {"id": "item5", "productId": "prodE", "productName": "Produto Echo", "quantity": 1, "unitPrice": 35.50, "totalPrice": 35.50},
        ]
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00004",
        "customer": {"id": "cust4", "name": "João Santos", "email": "joao.santos@example.com"},
        "orderDate": (datetime.now() - timedelta(days=5)).isoformat() + "Z",
        "totalAmount": 310.20, "status": "Pendente", "itemCount": 3
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00005",
        "customer": {"id": "cust5", "name": "Luiza Costa", "email": "luiza.costa@example.com"},
        "orderDate": (datetime.now() - timedelta(days=10)).isoformat() + "Z",
        "totalAmount": 55.00, "status": "Cancelado", "itemCount": 1
    },
    # Adicionando mais pedidos para testar paginação
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00006",
        "customer": {"id": "cust6", "name": "Pedro Almeida", "email": "pedro.a@example.com"},
        "orderDate": (datetime.now() - timedelta(days=3)).isoformat() + "Z",
        "totalAmount": 175.00, "status": "Processando", "itemCount": 2
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00007",
        "customer": {"id": "cust7", "name": "Beatriz Lima", "email": "bia.lima@example.com"},
        "orderDate": (datetime.now() - timedelta(days=4)).isoformat() + "Z",
        "totalAmount": 99.90, "status": "Enviado", "itemCount": 1
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00008",
        "customer": {"id": "cust8", "name": "Fernando Costa", "email": "fernando.c@example.com"},
        "orderDate": (datetime.now() - timedelta(days=1)).isoformat() + "Z",
        "totalAmount": 205.00, "status": "Pendente", "itemCount": 3
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00009",
        "customer": {"id": "cust9", "name": "Juliana Martins", "email": "juliana.m@example.com"},
        "orderDate": (datetime.now() - timedelta(days=6)).isoformat() + "Z",
        "totalAmount": 65.00, "status": "Entregue", "itemCount": 1
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00010",
        "customer": {"id": "cust10", "name": "Rafael Souza", "email": "rafael.s@example.com"},
        "orderDate": (datetime.now() - timedelta(days=7)).isoformat() + "Z",
        "totalAmount": 130.50, "status": "Cancelado", "itemCount": 2
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00011",
        "customer": {"id": "cust11", "name": "Sofia Silva", "email": "sofia.silva@example.com"},
        "orderDate": (datetime.now() - timedelta(days=2, hours=5)).isoformat() + "Z",
        "totalAmount": 450.00, "status": "Entregue", "itemCount": 4,
        "items": [
            {"id": str(uuid.uuid4()), "productId": "prodF", "productName": "Produto Foxtrot", "quantity": 2, "unitPrice": 200, "totalPrice": 400},
            {"id": str(uuid.uuid4()), "productId": "prodG", "productName": "Produto Golf", "quantity": 1, "unitPrice": 50, "totalPrice": 50},
        ]
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00012",
        "customer": {"id": "cust12", "name": "Lucas Gomes", "email": "lucas.gomes@example.com"},
        "orderDate": (datetime.now() - timedelta(days=1, hours=12)).isoformat() + "Z",
        "totalAmount": 90.00, "status": "Processando", "itemCount": 1
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00013",
        "customer": {"id": "cust13", "name": "Gabriela Rocha", "email": "gabriela.rocha@example.com"},
        "orderDate": (datetime.now() - timedelta(hours=6)).isoformat() + "Z",
        "totalAmount": 15.00, "status": "Pendente", "itemCount": 1
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00014",
        "customer": {"id": "cust14", "name": "Mateus Alves", "email": "mateus.alves@example.com"},
        "orderDate": (datetime.now() - timedelta(days=8)).isoformat() + "Z",
        "totalAmount": 500.00, "status": "Entregue", "itemCount": 5
    },
    {
        "id": str(uuid.uuid4()), "orderNumber": "ORD-2024-00015",
        "customer": {"id": "cust15", "name": "Larissa Dias", "email": "larissa.dias@example.com"},
        "orderDate": (datetime.now() - timedelta(days=15)).isoformat() + "Z",
        "totalAmount": 78.90, "status": "Cancelado", "itemCount": 1
    }
]

class OrderController:
    @staticmethod
    def get_orders():
        # Parâmetros de paginação e filtro
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_term = request.args.get('search', '', type=str).lower()
        status_filter = request.args.get('status', '', type=str)

        filtered_orders = MOCK_ORDERS_DATA

        if status_filter:
            filtered_orders = [order for order in filtered_orders if order['status'] == status_filter]

        if search_term:
            filtered_orders = [
                order for order in filtered_orders if
                search_term in order['orderNumber'].lower() or
                search_term in order['customer']['name'].lower() or
                search_term in order['customer']['email'].lower() or
                search_term in str(order['totalAmount']).lower()
            ]
        
        # Ordenar por data (mais recentes primeiro)
        filtered_orders.sort(key=lambda o: datetime.fromisoformat(o['orderDate'].replace('Z', '')), reverse=True)

        # Paginação
        total_orders = len(filtered_orders)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_orders = filtered_orders[start:end]

        return jsonify({
            "orders": paginated_orders,
            "page": page,
            "per_page": per_page,
            "total_orders": total_orders,
            "total_pages": (total_orders + per_page - 1) // per_page
        }), 200

    @staticmethod
    def get_order_by_id(order_id):
        order = next((order for order in MOCK_ORDERS_DATA if order['id'] == order_id), None)
        if order:
            # Simular carregamento de itens detalhados se não estiverem presentes no mock principal
            if 'items' not in order and order['id'] == "ORD-2024-00004": # Exemplo
                 order['items'] = [
                    {"id": str(uuid.uuid4()), "productId": "prodH", "productName": "Produto Hotel", "quantity": 2, "unitPrice": 100, "totalPrice": 200},
                    {"id": str(uuid.uuid4()), "productId": "prodI", "productName": "Produto India", "quantity": 1, "unitPrice": 110.20, "totalPrice": 110.20},
                 ]
            return jsonify(order), 200
        return jsonify({"message": "Pedido não encontrado"}), 404

    @staticmethod
    def update_order_status(order_id):
        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            return jsonify({"message": "Status não fornecido"}), 400

        order_idx = next((idx for idx, order in enumerate(MOCK_ORDERS_DATA) if order['id'] == order_id), None)

        if order_idx is not None:
            MOCK_ORDERS_DATA[order_idx]['status'] = new_status
            MOCK_ORDERS_DATA[order_idx]['orderDate'] = datetime.now().isoformat() + "Z" # Atualiza data para refletir modificação
            return jsonify(MOCK_ORDERS_DATA[order_idx]), 200
        
        return jsonify({"message": "Pedido não encontrado para atualização"}), 404

    # No futuro, poderíamos adicionar criar e deletar
    # @staticmethod
    # def create_order():
    #     # ... lógica para criar novo pedido ...
    #     pass

    # @staticmethod
    # def delete_order(order_id):
    #     # ... lógica para deletar pedido ...
    #     pass

# Não é necessário um blueprint aqui, pois o faremos em order_routes.py
# order_controller_bp = Blueprint('order_controller', __name__)
# order_controller_bp.route('/orders', methods=['GET'])(OrderController.get_orders)
# etc. 