from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required
from typing import Any
from decimal import Decimal

bp = Blueprint('payments', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/payments', methods=['POST'])
def create_payment() -> tuple[Any, int]:

    def map_items(item):
        return { 
            'id': item['produto']['id'], 
            'title': item['produto']['name'],
            'unit_price': item['produto']['price'], 
            'quantity': item['quantity'], 
            'currency_id': 'BRL'  
         }

    try:
        data = request.get_json()
        
        # Cria o pagamento no Mercado Pago
        payment_data = {
            'items': list(map(map_items, data.get('items'))),
        }
        
        mercadopago_payment = controller.payments.sdk.preference().create(payment_data)
        
        if mercadopago_payment['status'] != 201:
            return jsonify({'message': 'Erro ao processar pagamento no Mercado Pago' }), 400
        
        mp_response = mercadopago_payment['response']
        
        payment = controller.payments.create_payment(
            order_id=data.get('order_id'),
            payment_method=data.get('payment_method'),
            amount=Decimal(str(data.get('amount'))),
            transaction_id=mp_response['id']
        )
        
        return jsonify({
            'message': 'Pagamento registrado com sucesso', 
            'id': payment.id,
            'status': payment.status,
            'mercadopago_id': mp_response['id'],
            'url_payament': mp_response['init_point'],
            'data_mp': mp_response
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

@bp.route('/payments/webhook', methods=['POST'])
def webhook() -> tuple[Any, int]:
    try:
        data = request.get_json()
        
        if data['type'] == 'payment':
            payment_info = controller.payments.sdk.payment().get(data['data']['id'])
            
            if payment_info['status'] == 200:
                mp_payment = payment_info['response']
                
                # Busca o pagamento pelo transaction_id (que é o ID do Mercado Pago)
                payment = controller.payments.get_by_transaction_id(str(mp_payment['id']))
                
                if payment:
                    # Mapeia o status do Mercado Pago para o nosso sistema
                    status_mapping = {
                        'approved': 'Aprovado',
                        'pending': 'Pendente',
                        'in_process': 'Em Processamento',
                        'rejected': 'Rejeitado',
                        'cancelled': 'Cancelado',
                        'refunded': 'Reembolsado'
                    }
                    
                    new_status = status_mapping.get(mp_payment['status'], 'Pendente')
                    controller.payments.update_payment_status(payment.id, new_status)
                    
                    return jsonify({'message': 'Webhook processado com sucesso'}), 200
        
        return jsonify({'message': 'Webhook recebido'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500 