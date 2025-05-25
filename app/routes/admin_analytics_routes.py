from flask import Blueprint
from app.controllers.admin_analytics_controller import AdminAnalyticsController
from app.utils.decorators import admin_required

bp = Blueprint('admin_analytics', __name__, url_prefix='/admin/analytics')

@bp.route('/sales-by-category', methods=['GET'])
@admin_required()
def sales_by_category():
    return AdminAnalyticsController.get_sales_by_category_mock_data()

@bp.route('/total-sales', methods=['GET'])
@admin_required()
def total_sales():
    """
    Endpoint para dados de vendas totais
    Aceita parâmetros: start_date, end_date (formato: YYYY-MM-DD)
    """
    return AdminAnalyticsController.get_total_sales_data()

@bp.route('/total-orders', methods=['GET'])
@admin_required()
def total_orders():
    """
    Endpoint para dados de pedidos totais
    Aceita parâmetros: start_date, end_date (formato: YYYY-MM-DD)
    """
    return AdminAnalyticsController.get_total_orders_data()