from flask import jsonify, request
from flask import jsonify, request
from datetime import datetime, timedelta
from decimal import Decimal

# Dados fictícios fixos para Ticket Médio
mock_ticket_medio_evolution_data = [
  { "data": "11/Jul", "valor": 140.00 }, { "data": "12/Jul", "valor": 145.00 },
  { "data": "13/Jul", "valor": 142.00 }, { "data": "14/Jul", "valor": 148.00 },
  { "data": "15/Jul", "valor": 152.00 }, { "data": "16/Jul", "valor": 150.00 },
  { "data": "17/Jul", "valor": 158.00 }, { "data": "18/Jul", "valor": 155.00 },
  { "data": "19/Jul", "valor": 162.00 }, { "data": "20/Jul", "valor": 165.00 },
]

mock_products_impact_ticket_data = [
  { "id": "PROD1001", "nome": "Super Ração Premium", "valorMedioAdicionado": 55.75, "imagemUrl": "/images/backend-prod-placeholder1.svg" },
  { "id": "PROD1002", "nome": "Kit Jardinagem Expert", "valorMedioAdicionado": 42.10, "imagemUrl": "/images/backend-prod-placeholder2.svg" },
  { "id": "PROD1003", "nome": "Sementes Raras Importadas", "valorMedioAdicionado": 33.50, "imagemUrl": "/images/backend-prod-placeholder3.svg" },
  { "id": "PROD1004", "nome": "Adubo Orgânico Concentrado", "valorMedioAdicionado": 25.00, "imagemUrl": "/images/backend-prod-placeholder4.svg" },
]

mock_ticket_medio_summary_data = {
    "value": "R$ 155,20", 
    "subtitle": "Ticket Médio Atual",
    "trend": "+5.5%",
    "trendDirection": "up"
}

# Dados fictícios fixos para Taxa de Conversão
mock_conversion_funnel_data = [
  { "stage": "Visitantes", "value": 15000, "color": "#3b82f6" },
  { "stage": "Visualizaram Produto", "value": 9000, "color": "#22d3ee" },
  { "stage": "Adicionaram Carrinho", "value": 3000, "color": "#a3e635" },
  { "stage": "Concluíram Compra", "value": 1200, "color": "#22c55e" },
]

mock_conversion_optimizations_data = [
  { "id": 1, "texto": "Melhoria na velocidade da página de produto (+5% conversão)", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 2, "texto": "Checkout simplificado resultou em +3% na finalização.", "tipo": "sucesso", "iconName": "Zap" },
  { "id": 3, "texto": "Investigar abandono de carrinho na seleção de frete.", "tipo": "alerta", "iconName": "AlertOctagon" },
  { "id": 4, "texto": "Nova campanha de e-mail marketing iniciada.", "tipo": "info", "iconName": "MailCheck" }
]

mock_conversion_summary_data = {
    "value": "8.0%",
    "subtitle": "Taxa de Conversão",
    "trend": "+0.5%",
    "trendDirection": "up"
}

# Dados fictícios fixos para Visitantes Únicos
mock_visitantes_unicos_evolution_data = [
  { "dia": "01/07", "visitantes": 400 }, { "dia": "02/07", "visitantes": 450 },
  { "dia": "03/07", "visitantes": 420 }, { "dia": "04/07", "visitantes": 550 },
  { "dia": "05/07", "visitantes": 500 }, { "dia": "06/07", "visitantes": 600 },
  { "dia": "07/07", "visitantes": 580 }, { "dia": "08/07", "visitantes": 750 },
  { "dia": "09/07", "visitantes": 700 }, { "dia": "10/07", "visitantes": 800 },
]

mock_fontes_trafego_data = [
  { "nome": "Busca Orgânica", "visitantes": 6000, "percentual": 40, "iconName": "Search" },
  { "nome": "Tráfego Direto", "visitantes": 3500, "percentual": 23, "iconName": "Globe" },
  { "nome": "Redes Sociais", "visitantes": 3000, "percentual": 20, "iconName": "Users" },
  { "nome": "Referências", "visitantes": 2500, "percentual": 17, "iconName": "Link2" },
]

mock_visitantes_unicos_summary_cards_data = {
    "totalVisitantes": 15000,
    "visitantesRecorrentesPercentual": 40, 
    "novasSessoesPercentual": 60, 
    "taxaRejeicaoPercentual": 38 
}

class AdminAnalyticsController:
    # --- Métodos para o Dashboard Principal do Admin (Dados Fixos) ---
    @staticmethod
    def get_dashboard_summary_data():
        return jsonify({
            "activeUsers": 1500,
            "totalSalesCount": 750,
            "totalRevenue": 65000.00,
            "productCount": 250
        }), 200

    @staticmethod
    def get_monthly_sales_data():
        monthly_data = [
            {"month": "Jan", "sales": 7000.00, "revenue": 9000.00},
            {"month": "Fev", "sales": 6500.00, "revenue": 8500.00},
            {"month": "Mar", "sales": 8500.00, "revenue": 10500.00},
            {"month": "Abr", "sales": 7800.00, "revenue": 9800.00},
            {"month": "Mai", "sales": 10000.00, "revenue": 12000.00},
            {"month": "Jun", "sales": 9200.00, "revenue": 11500.00},
        ]
        return jsonify(monthly_data), 200

    @staticmethod
    def get_recent_sales_data():
        recent_sales = [
            {"id": "ORD-001", "customer": "João Silva", "date": "2024-07-27", "total": 150.00, "status": "Concluído"},
            {"id": "ORD-002", "customer": "Maria Oliveira", "date": "2024-07-26", "total": 85.50, "status": "Pendente"},
            {"id": "ORD-003", "customer": "Carlos Souza", "date": "2024-07-26", "total": 210.75, "status": "Concluído"},
            {"id": "ORD-004", "customer": "Ana Pereira", "date": "2024-07-25", "total": 55.00, "status": "Enviado"},
            {"id": "ORD-005", "customer": "Pedro Costa", "date": "2024-07-25", "total": 320.00, "status": "Concluído"},
            {"id": "ORD-006", "customer": "Luiza Santos", "date": "2024-07-24", "total": 99.90, "status": "Concluído"},
            {"id": "ORD-007", "customer": "Gabriel Lima", "date": "2024-07-24", "total": 180.00, "status": "Pendente"},
            {"id": "ORD-008", "customer": "Sofia Almeida", "date": "2024-07-23", "total": 75.20, "status": "Concluído"},
            {"id": "ORD-009", "customer": "Bruno Mendes", "date": "2024-07-23", "total": 250.00, "status": "Enviado"},
            {"id": "ORD-010", "customer": "Clara Ribeiro", "date": "2024-07-22", "total": 120.00, "status": "Concluído"},
        ]
        return jsonify(recent_sales), 200

    # --- Métodos existentes (Dados Fixos) ---
    @staticmethod
    def get_sales_by_category_mock_data():
        categories_agro = [
            "Fertilizantes", "Sementes de Milho", "Defensivos Agrícolas", 
            "Ferramentas Manuais", "Adubos Orgânicos", "Sistemas de Irrigação",
            "Rações Animal", "Sementes de Soja", "Máquinas Pequenas", "Veterinária"
        ]
        
        mock_data = []
        fixed_sales = [35000, 28000, 22000, 15000, 18000, 12000, 25000, 20000, 10000, 8000]
        fixed_transactions = [180, 120, 90, 60, 75, 50, 110, 85, 40, 30]

        for i, category in enumerate(categories_agro):
            mock_data.append({
                "categoryName": category,
                "totalSales": fixed_sales[i],
                "transactionCount": fixed_transactions[i]
            })
        return jsonify(mock_data), 200

    @staticmethod
    def get_recent_activities_mock_data():
        activities = [
            {"id": "act001", "tipo": "venda", "descricao": "Nova venda #PED1001 realizada", "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "detalhes": {"cliente": "Ana S.", "valor": 150.00}},
            {"id": "act002", "tipo": "usuario", "descricao": "Novo usuário registrado: Fernando A.", "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "detalhes": None},
            {"id": "act003", "tipo": "ticket", "descricao": "Ticket #TKT201 atualizado para: Resolvido", "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(), "detalhes": None},
            {"id": "act004", "tipo": "pagamento", "descricao": "Pagamento confirmado para pedido #PED1002", "timestamp": (datetime.now() - timedelta(minutes=20)).isoformat(), "detalhes": None},
            {"id": "act005", "tipo": "produto", "descricao": "Produto \"Tomate Orgânico\" atualizado", "timestamp": (datetime.now() - timedelta(minutes=25)).isoformat(), "detalhes": None},
            {"id": "act006", "tipo": "venda", "descricao": "Nova venda #PED1003 realizada", "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(), "detalhes": {"cliente": "Bruno L.", "valor": 250.50}},
            {"id": "act007", "tipo": "usuario", "descricao": "Novo usuário registrado: Gabriela M.", "timestamp": (datetime.now() - timedelta(hours=1, minutes=10)).isoformat(), "detalhes": None},
            {"id": "act008", "tipo": "ticket", "descricao": "Ticket #TKT202 atualizado para: Em Andamento", "timestamp": (datetime.now() - timedelta(hours=1, minutes=20)).isoformat(), "detalhes": None},
            {"id": "act009", "tipo": "pagamento", "descricao": "Pagamento confirmado para pedido #PED1004", "timestamp": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(), "detalhes": None},
            {"id": "act010", "tipo": "produto", "descricao": "Produto \"Alface Crespa\" atualizado", "timestamp": (datetime.now() - timedelta(hours=1, minutes=40)).isoformat(), "detalhes": None},
            {"id": "act011", "tipo": "venda", "descricao": "Nova venda #PED1005 realizada", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(), "detalhes": {"cliente": "Carla P.", "valor": 80.00}},
            {"id": "act012", "tipo": "usuario", "descricao": "Novo usuário registrado: Hugo R.", "timestamp": (datetime.now() - timedelta(hours=2, minutes=15)).isoformat(), "detalhes": None},
            {"id": "act013", "tipo": "ticket", "descricao": "Ticket #TKT203 atualizado para: Fechado", "timestamp": (datetime.now() - timedelta(hours=2, minutes=30)).isoformat(), "detalhes": None},
            {"id": "act014", "tipo": "pagamento", "descricao": "Pagamento confirmado para pedido #PED1006", "timestamp": (datetime.now() - timedelta(hours=2, minutes=45)).isoformat(), "detalhes": None},
            {"id": "act015", "tipo": "produto", "descricao": "Produto \"Cenoura Fresca\" atualizado", "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(), "detalhes": None},
            {"id": "act016", "tipo": "venda", "descricao": "Nova venda #PED1007 realizada", "timestamp": (datetime.now() - timedelta(hours=3, minutes=10)).isoformat(), "detalhes": {"cliente": "Daniel F.", "valor": 300.00}},
            {"id": "act017", "tipo": "usuario", "descricao": "Novo usuário registrado: Isabela C.", "timestamp": (datetime.now() - timedelta(hours=3, minutes=20)).isoformat(), "detalhes": None},
            {"id": "act018", "tipo": "ticket", "descricao": "Ticket #TKT204 atualizado para: Resolvido", "timestamp": (datetime.now() - timedelta(hours=3, minutes=30)).isoformat(), "detalhes": None},
            {"id": "act019", "tipo": "pagamento", "descricao": "Pagamento confirmado para pedido #PED1008", "timestamp": (datetime.now() - timedelta(hours=3, minutes=40)).isoformat(), "detalhes": None},
            {"id": "act020", "tipo": "produto", "descricao": "Produto \"Batata Doce\" atualizado", "timestamp": (datetime.now() - timedelta(hours=3, minutes=50)).isoformat(), "detalhes": None},
        ]
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(activities), 200

    # --- Métodos para Ticket Médio (Dados Fixos) ---
    @staticmethod
    def get_ticket_medio_evolution_data():
        return jsonify(mock_ticket_medio_evolution_data), 200

    @staticmethod
    def get_ticket_medio_products_impact_data():
        return jsonify(mock_products_impact_ticket_data), 200

    @staticmethod
    def get_ticket_medio_summary_data():
        return jsonify(mock_ticket_medio_summary_data), 200

    # --- Métodos para Taxa de Conversão (Dados Fixos) ---
    @staticmethod
    def get_conversion_funnel_data(): # Servirá o funil e as otimizações
        return jsonify({
            "funnelData": mock_conversion_funnel_data,
            "optimizations": mock_conversion_optimizations_data
        }), 200

    @staticmethod
    def get_conversion_summary_data():
        return jsonify(mock_conversion_summary_data), 200

    # --- Métodos para Visitantes Únicos (detalhes) (Dados Fixos) ---
    @staticmethod
    def get_visitantes_unicos_details_data():
        return jsonify({
            "evolutionData": mock_visitantes_unicos_evolution_data,
            "trafficSourcesData": mock_fontes_trafego_data,
            "summaryCardsData": mock_visitantes_unicos_summary_cards_data
        }), 200

    # --- Métodos da branch dvdweb2 (Dados Fixos) ---
    @staticmethod
    def get_total_sales_data():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        current_total = 750000.00
        previous_total = 700000.00
        
        trend_percentage = round(((current_total - previous_total) / previous_total) * 100, 2)
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        daily_sales = [100000, 110000, 105000, 120000, 115000, 100000, 100000] # 7 dias de vendas fixas
        
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
        
        current_orders = 3500
        previous_orders = 3200
        
        trend_percentage = round(((current_orders - previous_orders) / previous_orders) * 100, 2)
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        weekday_orders = [
            {"day": "Segunda", "orders": 500},
            {"day": "Terça", "orders": 550},
            {"day": "Quarta", "orders": 480},
            {"day": "Quinta", "orders": 600},
            {"day": "Sexta", "orders": 520},
            {"day": "Sábado", "orders": 400},
            {"day": "Domingo", "orders": 450}
        ]
        
        status_breakdown = {
            "completed": 2800,
            "pending": 500,
            "cancelled": 200
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
            { "mes": "Jan", "novosClientes": 60 },
            { "mes": "Fev", "novosClientes": 55 },
            { "mes": "Mar", "novosClientes": 80 },
            { "mes": "Abr", "novosClientes": 90 },
            { "mes": "Mai", "novosClientes": 70 },
            { "mes": "Jun", "novosClientes": 85 },
            { "mes": "Jul", "novosClientes": 100 },
        ]

        recent_customers_data = [
            {"id": "USR001", "nome": "Mariana Santos", "dataRegistro": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), "canal": "Orgânico"},
            {"id": "USR002", "nome": "Rafael Oliveira", "dataRegistro": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), "canal": "Referência"},
            {"id": "USR003", "nome": "Juliana Pereira", "dataRegistro": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), "canal": "Social"},
            {"id": "USR004", "nome": "Lucas Martins", "dataRegistro": (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'), "canal": "Campanha Email"},
            {"id": "USR005", "nome": "Beatriz Almeida", "dataRegistro": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "canal": "Direto"},
        ]

        total_novos_clientes_periodo = sum(item["novosClientes"] for item in monthly_new_customers_data)
        
        novos_clientes_mes_atual = monthly_new_customers_data[-1]["novosClientes"]
        novos_clientes_mes_anterior = monthly_new_customers_data[-2]["novosClientes"]
        crescimento_percentual = round(((novos_clientes_mes_atual - novos_clientes_mes_anterior) / novos_clientes_mes_anterior) * 100, 1)
            
        cpa_estimado = 18.50

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
