from flask import Blueprint
from app.controllers.admin_analytics_controller import AdminAnalyticsController
from app.utils.decorators import admin_required

bp = Blueprint('admin_analytics', __name__, url_prefix='/admin/analytics')

@bp.route('/sales-by-category', methods=['GET'])
@admin_required()
def sales_by_category():
    return AdminAnalyticsController.get_sales_by_category_mock_data() 