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