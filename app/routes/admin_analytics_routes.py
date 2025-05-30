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
def get_total_sales():
    return AdminAnalyticsController.get_total_sales_data()

@bp.route('/total-orders', methods=['GET'])
@admin_required()
def get_total_orders():
    return AdminAnalyticsController.get_total_orders_data()

@bp.route('/new-customers', methods=['GET'])
@admin_required()
def get_new_customers():
    return AdminAnalyticsController.get_new_customers_data()

@bp.route('/recent-activities', methods=['GET'])
@admin_required()
def get_recent_activities():
    return AdminAnalyticsController.get_recent_activities_mock_data()

# --- Rotas para Ticket Médio ---
@bp.route('/ticket-medio/evolution', methods=['GET'])
@admin_required()
def ticket_medio_evolution():
    return AdminAnalyticsController.get_ticket_medio_evolution_data()

@bp.route('/ticket-medio/products-impact', methods=['GET'])
@admin_required()
def ticket_medio_products_impact():
    return AdminAnalyticsController.get_ticket_medio_products_impact_data()

@bp.route('/ticket-medio/summary', methods=['GET'])
@admin_required()
def ticket_medio_summary():
    return AdminAnalyticsController.get_ticket_medio_summary_data()

# --- Rotas para Taxa de Conversão ---
@bp.route('/taxa-conversao/details', methods=['GET'])
@admin_required()
def taxa_conversao_details():
    return AdminAnalyticsController.get_conversion_funnel_data()

@bp.route('/taxa-conversao/summary', methods=['GET'])
@admin_required()
def taxa_conversao_summary():
    return AdminAnalyticsController.get_conversion_summary_data()

# --- Rotas para Visitantes Únicos (detalhes) ---
@bp.route('/visitantes-unicos/details', methods=['GET'])
@admin_required()
def visitantes_unicos_details():
    return AdminAnalyticsController.get_visitantes_unicos_details_data() 