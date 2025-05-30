from flask import Blueprint
from app.controllers.admin_analytics_controller import AdminAnalyticsController
from app.utils.decorators import admin_required

admin_analytics_bp = Blueprint('admin_analytics_bp', __name__, url_prefix='/admin/analytics')

@admin_analytics_bp.route('/sales-by-category', methods=['GET'])
@admin_required()
def sales_by_category():
    return AdminAnalyticsController.get_sales_by_category_mock_data()

@admin_analytics_bp.route('/recent-activities', methods=['GET'])
@admin_required()
def recent_activities():
    return AdminAnalyticsController.get_recent_activities_mock_data()

# --- Rotas movidas de advanced_analytics_routes.py ---

# Ticket Médio
@admin_analytics_bp.route('/ticket-medio/evolution', methods=['GET'])
@admin_required()
def get_ticket_medio_evolution():
    return AdminAnalyticsController.get_ticket_medio_evolution_data()

@admin_analytics_bp.route('/ticket-medio/products-impact', methods=['GET'])
@admin_required()
def get_products_impact_ticket():
    return AdminAnalyticsController.get_ticket_medio_products_impact_data()

@admin_analytics_bp.route('/ticket-medio/summary', methods=['GET'])
@admin_required()
def get_ticket_medio_summary():
    return AdminAnalyticsController.get_ticket_medio_summary_data()

# Taxa de Conversão
@admin_analytics_bp.route('/taxa-conversao/details', methods=['GET'])
@admin_required()
def get_taxa_conversao_details():
    return AdminAnalyticsController.get_conversion_funnel_data()

@admin_analytics_bp.route('/taxa-conversao/summary', methods=['GET'])
@admin_required()
def get_taxa_conversao_summary():
    return AdminAnalyticsController.get_conversion_summary_data()
