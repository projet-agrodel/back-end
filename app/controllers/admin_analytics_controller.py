from flask import jsonify, request
import random
from datetime import datetime, timedelta
from decimal import Decimal

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
    def get_total_sales_data():
        """
        Retorna dados de vendas totais com estrutura preparada para dados reais.
        TODO: Substituir por queries reais do banco quando em produção:
        - SELECT SUM(amount) FROM pagamento WHERE status = 'Aprovado' AND created_at BETWEEN start_date AND end_date
        """
        # Simular parâmetros de filtro de data (para estrutura futura)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Dados fictícios para visualização
        current_total = round(random.uniform(500000, 800000), 2)
        previous_total = round(current_total * random.uniform(0.85, 1.15), 2)
        
        # Calcular trend
        if previous_total > 0:
            trend_percentage = round(((current_total - previous_total) / previous_total) * 100, 2)
        else:
            trend_percentage = 0
        
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        # Dados para gráfico (últimos 7 dias de vendas)
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
        """
        Retorna dados de pedidos totais com estrutura preparada para dados reais.
        TODO: Substituir por queries reais do banco quando em produção:
        - SELECT COUNT(*) FROM pedido WHERE created_at BETWEEN start_date AND end_date
        """
        # Simular parâmetros de filtro de data (para estrutura futura)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Dados fictícios para visualização
        current_orders = random.randint(2500, 4500)
        previous_orders = random.randint(2000, 4000)
        
        # Calcular trend
        if previous_orders > 0:
            trend_percentage = round(((current_orders - previous_orders) / previous_orders) * 100, 2)
        else:
            trend_percentage = 0
        
        trend_direction = "up" if trend_percentage > 0 else "down" if trend_percentage < 0 else "neutral"
        
        # Dados para gráfico (pedidos por dia da semana)
        weekday_orders = []
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        for day in weekdays:
            day_orders = random.randint(200, 800)
            weekday_orders.append({
                "day": day,
                "orders": day_orders
            })
        
        # Status breakdown dos pedidos
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
        """
        Retorna dados mockados para a análise de novos clientes.
        TODO: Substituir por queries reais do banco quando em produção.
        """
        # Dados mockados para o gráfico de novos clientes por mês
        monthly_new_customers_data = [
            { "mes": "Jan", "novosClientes": random.randint(50, 80) },
            { "mes": "Fev", "novosClientes": random.randint(40, 70) },
            { "mes": "Mar", "novosClientes": random.randint(70, 100) },
            { "mes": "Abr", "novosClientes": random.randint(75, 110) },
            { "mes": "Mai", "novosClientes": random.randint(50, 80) },
            { "mes": "Jun", "novosClientes": random.randint(65, 95) },
            { "mes": "Jul", "novosClientes": random.randint(80, 120) }, # Mês atual (simulado)
        ]

        # Dados mockados para clientes recentes
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

        # Métricas agregadas
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
            
        cpa_estimado = round(random.uniform(10, 25), 2) # Custo por Aquisição Estimado (simulado)

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