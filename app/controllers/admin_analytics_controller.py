from flask import jsonify, request
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Dados fictícios para Ticket Médio (da branch HEAD)
mock_ticket_medio_evolution_data = [
  { "data": "11/Jul", "valor": 138.50 }, { "data": "12/Jul", "valor": 142.30 },
  { "data": "13/Jul", "valor": 139.90 }, { "data": "14/Jul", "valor": 145.60 },
  { "data": "15/Jul", "valor": 150.10 }, { "data": "16/Jul", "valor": 148.75 },
  { "data": "17/Jul", "valor": 155.20 }, { "data": "18/Jul", "valor": 152.40 },
  { "data": "19/Jul", "valor": 160.00 }, { "data": "20/Jul", "valor": 160.50 },
]

mock_products_impact_ticket_data = [
  { "id": "PROD1001", "nome": "Super Ração Premium", "valorMedioAdicionado": 55.75, "imagemUrl": "/images/backend-prod-placeholder1.svg" },
  { "id": "PROD1002", "nome": "Kit Jardinagem Expert", "valorMedioAdicionado": 42.10, "imagemUrl": "/images/backend-prod-placeholder2.svg" },
  { "id": "PROD1003", "nome": "Sementes Raras Importadas", "valorMedioAdicionado": 33.50, "imagemUrl": "/images/backend-prod-placeholder3.svg" },
  { "id": "PROD1004", "nome": "Adubo Orgânico Concentrado", "valorMedioAdicionado": 25.00, "imagemUrl": "/images/backend-prod-placeholder4.svg" },
]

mock_ticket_medio_summary_data = {
    "value": "R$ 999,99", 
    "subtitle": "Ticket (Backend Novo Teste)",
    "trend": "++10.0% TEST",
    "trendDirection": "up"
}

# Dados fictícios para Taxa de Conversão (da branch HEAD)
mock_conversion_funnel_data = [
  { "stage": "Visitantes", "value": 13500, "color": "#3b82f6" },
  { "stage": "Visualizaram Produto", "value": 8200, "color": "#22d3ee" },
  { "stage": "Adicionaram Carrinho", "value": 2800, "color": "#a3e635" },
  { "stage": "Concluíram Compra", "value": 1150, "color": "#22c55e" },
]

mock_conversion_optimizations_data = [
  { "id": 1, "texto": "Backend: Melhoria na velocidade da página de produto (+5% conversão)", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 2, "texto": "Backend: Checkout simplificado resultou em +3% na finalização.", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 3, "texto": "Backend: Investigar abandono de carrinho na seleção de frete.", "tipo": "alerta", "iconName": "AlertOctagon" },
  { "id": 4, "texto": "Backend: Nova campanha de e-mail marketing iniciada.", "tipo": "info", "iconName": "MailCheck" }
]

mock_conversion_summary_data = {
    "value": "25.0% TEST",
    "subtitle": "Conversão (Backend Teste)",
    "trend": "--5.0% TEST",
    "trendDirection": "down"
}

mock_visitantes_unicos_evolution_data = [
  { "dia": "01/07", "visitantes": 350 }, { "dia": "02/07", "visitantes": 410 },
  { "dia": "03/07", "visitantes": 380 }, { "dia": "04/07", "visitantes": 520 },
  { "dia": "05/07", "visitantes": 480 }, { "dia": "06/07", "visitantes": 610 },
  { "dia": "07/07", "visitantes": 550 }, { "dia": "08/07", "visitantes": 700 },
  { "dia": "09/07", "visitantes": 650 }, { "dia": "10/07", "visitantes": 720 },
]

mock_fontes_trafego_data = [
  { "nome": "Busca Orgânica", "visitantes": 5800, "percentual": 45, "iconName": "Search" },
  { "nome": "Tráfego Direto", "visitantes": 3200, "percentual": 25, "iconName": "Globe" },
  { "nome": "Redes Sociais", "visitantes": 2500, "percentual": 19, "iconName": "Users" },
  { "nome": "Referências", "visitantes": 1500, "percentual": 11, "iconName": "Link2" },
]

mock_visitantes_unicos_summary_cards_data = {
    "totalVisitantes": sum(item['visitantes'] for item in mock_visitantes_unicos_evolution_data),
    "visitantesRecorrentesPercentual": 35, 
    "novasSessoesPercentual": 65, 
    "taxaRejeicaoPercentual": 42 
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

        for i in range(1, 21): 
            activity_type = random.choice(activity_types)
            
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
                "timestamp": timestamp.isoformat(),
                "detalhes": details
            })
        
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(activities), 200

    # --- Métodos para Ticket Médio (da branch HEAD) ---
    @staticmethod
    def get_ticket_medio_evolution_data():
        return jsonify(mock_ticket_medio_evolution_data), 200

    @staticmethod
    def get_ticket_medio_products_impact_data():
        return jsonify(mock_products_impact_ticket_data), 200

    @staticmethod
    def get_ticket_medio_summary_data():
        return jsonify(mock_ticket_medio_summary_data), 200

    # --- Métodos para Taxa de Conversão (da branch HEAD) ---
    @staticmethod
    def get_conversion_funnel_data(): # Servirá o funil e as otimizações
        return jsonify({
            "funnelData": mock_conversion_funnel_data,
            "optimizations": mock_conversion_optimizations_data
        }), 200

    @staticmethod
    def get_conversion_summary_data():
        return jsonify(mock_conversion_summary_data), 200

    # --- Métodos para Visitantes Únicos (detalhes) ---
    @staticmethod
    def get_visitantes_unicos_details_data():
        return jsonify({
            "evolutionData": mock_visitantes_unicos_evolution_data,
            "trafficSourcesData": mock_fontes_trafego_data,
            "summaryCardsData": mock_visitantes_unicos_summary_cards_data
        }), 200

    # --- Métodos da branch dvdweb2 ---
    @staticmethod
    def get_total_sales_data():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        current_total = round(random.uniform(500000, 800000), 2)
        previous_total = round(current_total * random.uniform(0.85, 1.15), 2)
        
        if previous_total > 0:
            trend_percentage = round(((current_total - previous_total) / previous_total) * 100, 2)
        else:
            trend_percentage = 0
        
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        daily_sales = []
        for i in range(7):
            day_sales = round(random.uniform(50000, 120000), 2)
            daily_sales.append(day_sales)
        
        return jsonify({
            "total_sales": current_total,
            "previous_period_sales": previous_total,
            "trend_percentage": abs(trend_percentage),
            "trend_direction": trend_direction,
            "currency": "BRL",
            "period": {
                "start_date": start_date or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                "end_date": end_date or datetime.now().strftime('%Y-%m-%d')
            },
            "daily_sales_chart": daily_sales,
            "formatted_total": f"R$ {current_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "last_updated": datetime.now().isoformat()
        }), 200
    
    @staticmethod
    def get_total_orders_data():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        current_orders = random.randint(2500, 4500)
        previous_orders = random.randint(2000, 4000)
        
        if previous_orders > 0:
            trend_percentage = round(((current_orders - previous_orders) / previous_orders) * 100, 2)
        else:
            trend_percentage = 0
        
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        weekday_orders = []
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        for day in weekdays:
            day_orders = random.randint(200, 800)
            weekday_orders.append({
                "day": day,
                "orders": day_orders
            })
        
        status_breakdown = {
            "completed": random.randint(int(current_orders * 0.7), int(current_orders * 0.85)),
            "pending": random.randint(int(current_orders * 0.1), int(current_orders * 0.2)),
            "cancelled": random.randint(int(current_orders * 0.05), int(current_orders * 0.15))
        }
        
        return jsonify({
            "total_orders": current_orders,
            "previous_period_orders": previous_orders,
            "trend_percentage": abs(trend_percentage),
            "trend_direction": trend_direction,
            "period": {
                "start_date": start_date or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                "end_date": end_date or datetime.now().strftime('%Y-%m-%d')
            },
            "weekday_orders_chart": weekday_orders,
            "status_breakdown": status_breakdown,
            "average_orders_per_day": round(current_orders / 30, 1),
            "last_updated": datetime.now().isoformat()
        }), 200

    @staticmethod
    def get_new_customers_data():
        monthly_new_customers_data = [
            { "mes": "Jan", "novosClientes": random.randint(50, 80) },
            { "mes": "Fev", "novosClientes": random.randint(40, 70) },
            { "mes": "Mar", "novosClientes": random.randint(70, 100) },
            { "mes": "Abr", "novosClientes": random.randint(75, 110) },
            { "mes": "Mai", "novosClientes": random.randint(50, 80) },
            { "mes": "Jun", "novosClientes": random.randint(65, 95) },
            { "mes": "Jul", "novosClientes": random.randint(80, 120) },
        ]

        recent_customers_data = []
        first_names = ["Mariana", "Rafael", "Juliana", "Lucas", "Beatriz", "Carlos", "Fernanda", "Ricardo", "Patricia", "Gustavo"]
        last_names = ["Santos", "Oliveira", "Pereira", "Martins", "Almeida", "Costa", "Souza", "Lima", "Carvalho", "Rodrigues"]
        channels = ["Orgânico", "Referência", "Social", "Campanha Email", "Direto"]
        
        for i in range(5):
            days_ago = random.randint(1, 10)
            recent_customers_data.append({
                "id": f"USR{random.randint(100, 999):03d}",
                "nome": f"{random.choice(first_names)} {random.choice(last_names)}",
                "dataRegistro": (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d'),
                "canal": random.choice(channels)
            })

        total_novos_clientes_periodo = sum(item["novosClientes"] for item in monthly_new_customers_data)
        
        if len(monthly_new_customers_data) >= 2:
            novos_clientes_mes_atual = monthly_new_customers_data[-1]["novosClientes"]
            novos_clientes_mes_anterior = monthly_new_customers_data[-2]["novosClientes"]
            if novos_clientes_mes_anterior > 0:
                crescimento_percentual = round(((novos_clientes_mes_atual - novos_clientes_mes_anterior) / novos_clientes_mes_anterior) * 100, 1)
            else:
                crescimento_percentual = 0
        else:
            crescimento_percentual = 0
            
        cpa_estimado = round(random.uniform(10, 25), 2)

        return jsonify({
            "monthly_new_customers_chart": monthly_new_customers_data,
            "recent_customers": recent_customers_data,
            "summary_metrics": {
                "total_new_customers_period": total_novos_clientes_periodo,
                "growth_percentage_vs_previous_month": crescimento_percentual,
                "estimated_cpa_brl": cpa_estimado
            },
            "last_updated": datetime.now().isoformat()
        }), 200
