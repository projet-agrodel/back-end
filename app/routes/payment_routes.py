from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any
from decimal import Decimal
import uuid

bp = Blueprint('payments', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/payments', methods=['POST'])
def create_payment() -> tuple[Any, int]:
    try:
        data = request.get_json()        
        order_id = data.get('order_id')

        payment = controller.payments.create_payment(
            order_id=order_id,
            payment_method=data.get('payment_method'),
            amount=Decimal(str(data.get('amount'))),
            transaction_id=str(uuid.uuid4())
        )

        return jsonify({
            'message': 'Pagamento registrado com sucesso',
            'payament': payment.to_dict(),
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/payments/order/<int:order_id>', methods=['GET'])
def get_order_payments(order_id: int) -> tuple[Any, int]:
    try:
        payments = controller.payments.get_order_payments(order_id)
        return jsonify([payment.to_dict() for payment in payments]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/payments/<int:payment_id>/status', methods=['PUT'])
def update_payment_status(payment_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'message': 'Status é obrigatório'}), 400
            
        payment = controller.payments.update_payment_status(payment_id, status)
        
        if not payment:
            return jsonify({'message': 'Pagamento não encontrado'}), 404
            
        return jsonify({
            'message': 'Status do pagamento atualizado com sucesso',
            'status': payment.status
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/payments/pending', methods=['GET'])
def get_pending_payments() -> tuple[Any, int]:
    try:
        payments = controller.payments.get_pending_payments()
        return jsonify([payment.to_dict() for payment in payments]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500 