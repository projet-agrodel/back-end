from flask import jsonify
import random
from datetime import datetime, timedelta

# Dados fictícios para Ticket Médio e Taxa de Conversão (movidos para cá)
mock_ticket_medio_evolution_data = [
  { "data": "11/Jul", "valor": 138.50 }, { "data": "12/Jul", "valor": 142.30 },
  { "data": "13/Jul", "valor": 139.90 }, { "data": "14/Jul", "valor": 145.60 },
  { "data": "15/Jul", "valor": 150.10 }, { "data": "16/Jul", "valor": 148.75 },
  { "data": "17/Jul", "valor": 155.20 }, { "data": "18/Jul", "valor": 152.40 },
  { "data": "19/Jul", "valor": 160.00 }, { "data": "20/Jul", "valor": 158.50 },
]

mock_products_impact_ticket_data = [
  { "id": "PROD1001", "nome": "Super Ração Premium", "valorMedioAdicionado": 55.75, "imagemUrl": "/images/backend-prod-placeholder1.svg" },
  { "id": "PROD1002", "nome": "Kit Jardinagem Expert", "valorMedioAdicionado": 42.10, "imagemUrl": "/images/backend-prod-placeholder2.svg" },
  { "id": "PROD1003", "nome": "Sementes Raras Importadas", "valorMedioAdicionado": 33.50, "imagemUrl": "/images/backend-prod-placeholder3.svg" },
  { "id": "PROD1004", "nome": "Adubo Orgânico Concentrado", "valorMedioAdicionado": 25.00, "imagemUrl": "/images/backend-prod-placeholder4.svg" },
]

mock_ticket_medio_summary_data = {
    "value": "R$ 999,99", # Usando os valores de teste mais recentes
    "subtitle": "Ticket (Backend Novo Teste)",
    "trend": "++10.0% TEST",
    "trendDirection": "up"
}

mock_conversion_funnel_data = [
  { "stage": "Visitantes (Backend)", "value": 13500, "color": "#3b82f6" },
  { "stage": "Visualizaram Produto (Backend)", "value": 8200, "color": "#22d3ee" },
  { "stage": "Adicionaram Carrinho (Backend)", "value": 2800, "color": "#a3e635" },
  { "stage": "Concluíram Compra (Backend)", "value": 1150, "color": "#22c55e" },
]

mock_conversion_optimizations_data = [
  { "id": 1, "texto": "Backend: Melhoria na velocidade da página de produto (+5% conversão)", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 2, "texto": "Backend: Checkout simplificado resultou em +3% na finalização.", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 3, "texto": "Backend: Investigar abandono de carrinho na seleção de frete.", "tipo": "alerta", "iconName": "AlertOctagon" },
  { "id": 4, "texto": "Backend: Nova campanha de e-mail marketing iniciada.", "tipo": "info", "iconName": "MailCheck" }
]

mock_conversion_summary_data = {
    "value": "25.0% TEST", # Usando os valores de teste mais recentes
    "subtitle": "Conversão (Backend Teste)",
    "trend": "--5.0% TEST",
    "trendDirection": "down"
}


class AdminAnalyticsController:
    @staticmethod
    def get_sales_by_category_mock_data():
        categories_agro = [
            "Fertilizantes", "Sementes de Milho", "Defensivos Agrícolas", 
            "Ferramentas Manuais", "Adubos Orgânicos", "Sistemas de Irrigação",
            "Rações Animal", "Sementes de Soja", "Máquinas Pequenas", "Veterinária"
        ]
        
        mock_data = []
        for category in categories_agro:
            total_sales = round(random.uniform(5000, 30000), 2)
            transaction_count = random.randint(20, 150)
            mock_data.append({
                "categoryName": category,
                "totalSales": total_sales,
                "transactionCount": transaction_count
            })
            
        # Simular algumas categorias com vendas maiores ou menores para dar variedade
        # Exemplo: Fertilizantes e Defensivos com mais vendas
        for item in mock_data:
            if item["categoryName"] == "Fertilizantes":
                item["totalSales"] = round(random.uniform(20000, 50000), 2)
                item["transactionCount"] = random.randint(100, 250)
            elif item["categoryName"] == "Defensivos Agrícolas":
                item["totalSales"] = round(random.uniform(18000, 45000), 2)
                item["transactionCount"] = random.randint(90, 220)
            elif item["categoryName"] == "Rações Animal":
                 item["totalSales"] = round(random.uniform(10000, 35000), 2)
                 item["transactionCount"] = random.randint(80, 200)

        
        return jsonify(mock_data), 200

    @staticmethod
    def get_recent_activities_mock_data():
        activities = []
        now = datetime.now()

        activity_types = [
            {'type': 'venda', 'description_template': 'Nova venda #PED{} realizada', 'details_template': {'cliente': 'Cliente {}', 'valor': random.uniform(50, 500)}},
            {'type': 'usuario', 'description_template': 'Novo usuário registrado: {}', 'details_template': None},
            {'type': 'ticket', 'description_template': 'Ticket #TKT{} atualizado para: {}', 'details_template': None},
            {'type': 'pagamento', 'description_template': 'Pagamento confirmado para pedido #PED{}', 'details_template': None},
            {'type': 'produto', 'description_template': 'Produto "{}" atualizado', 'details_template': None},
        ]

        for i in range(1, 21): # Gerar 20 atividades fictícias
            activity_type = random.choice(activity_types)
            
            # Gerar timestamp aleatório nas últimas 24 horas
            minutes_ago = random.randint(1, 24 * 60)
            timestamp = now - timedelta(minutes=minutes_ago)

            description = ""
            details = None

            if activity_type['type'] == 'venda':
                order_id = 1000 + i
                client_name = random.choice(['Ana S.', 'Bruno L.', 'Carla P.', 'Daniel F.', 'Elena G.'])
                value = round(random.uniform(50, 500), 2)
                description = activity_type['description_template'].format(order_id)
                details = {'cliente': client_name, 'valor': value}
            elif activity_type['type'] == 'usuario':
                user_name = random.choice(['Fernando A.', 'Gabriela M.', 'Hugo R.', 'Isabela C.', 'João V.'])
                description = activity_type['description_template'].format(user_name)
            elif activity_type['type'] == 'ticket':
                ticket_id = 200 + i
                status = random.choice(['Resolvido', 'Em Andamento', 'Fechado'])
                description = activity_type['description_template'].format(ticket_id, status)
            elif activity_type['type'] == 'pagamento':
                order_id = 1000 + i
                description = activity_type['description_template'].format(order_id)
            elif activity_type['type'] == 'produto':
                product_name = random.choice(['Tomate Orgânico', 'Alface Crespa', 'Cenoura Fresca', 'Batata Doce', 'Pimentão Verde'])
                description = activity_type['description_template'].format(product_name)

            activities.append({
                "id": f"act{i:03d}",
                "tipo": activity_type['type'],
                "descricao": description,
                "timestamp": timestamp.isoformat(), # Formato ISO para fácil parse no frontend
                "detalhes": details
            })
        
        # Ordenar as atividades pela mais recente
        activities.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify(activities), 200

    # --- Métodos para Ticket Médio ---
    @staticmethod
    def get_ticket_medio_evolution_data():
        return jsonify(mock_ticket_medio_evolution_data), 200

    @staticmethod
    def get_ticket_medio_products_impact_data():
        return jsonify(mock_products_impact_ticket_data), 200

    @staticmethod
    def get_ticket_medio_summary_data():
        return jsonify(mock_ticket_medio_summary_data), 200

    # --- Métodos para Taxa de Conversão ---
    @staticmethod
    def get_conversion_funnel_data(): # Este método servirá o funil e as otimizações juntas
        return jsonify({
            "funnelData": mock_conversion_funnel_data,
            "optimizations": mock_conversion_optimizations_data
        }), 200

    @staticmethod
    def get_conversion_summary_data():
        return jsonify(mock_conversion_summary_data), 200
