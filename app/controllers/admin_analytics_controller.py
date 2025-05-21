from flask import jsonify
import random

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