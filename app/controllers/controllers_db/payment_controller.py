from typing import List, Optional
from app.models.payment import Payment
from app.models.order import Order
from app.controllers.base.base_controller import BaseController
from decimal import Decimal
from mercadopago import SDK
import os

class PaymentController(BaseController[Payment]):

    def __init__(self) -> None:
        super().__init__(Payment)
        self.sdk = SDK(os.environ.get('SDK_KEY'))

    def create_payment(
        self, 
        order_id: int, 
        payment_method: str, 
        amount: Decimal,
        transaction_id: str
    ) -> Payment:
        try:
            order = Order.query.get_or_404(order_id)
            
            if order.amount != amount:
                raise ValueError("Valor do pagamento diferente do valor do pedido")

            payment = self.create({
                'pedido_id': order_id,
                'payment_method': payment_method,
                'status': 'Pendente',
                'amount': amount,
                'transaction_id': transaction_id
            })

            return payment
        except Exception as e:
            self._db.session.rollback()
            raise e

    def update_payment_status(self, payment_id: int, status: str) -> Optional[Payment]:
        try:
            payment = self.get_by_id(payment_id)
            if payment:
                payment.status = status
                self._db.session.commit()
            return payment
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_order_payments(self, order_id: int) -> List[Payment]:
        return self.get_query().filter_by(pedido_id=order_id).all()

    def get_pending_payments(self) -> List[Payment]:
        return self.get_query().filter_by(status='Pendente').all()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        return self.get_query().filter_by(transaction_id=transaction_id).first()

    def check_payment_status(self, payment_id: int) -> dict:
        try:
            payment = self.get_by_id(payment_id)
            if not payment:
                return {'error': 'Pagamento não encontrado'}

            # Consulta o status do pagamento no Mercado Pago
            payment_info = self.sdk.payment().get(payment.transaction_id)
            
            if payment_info['status'] == 200:
                mp_payment = payment_info['response']
                return {
                    'status': mp_payment['status'],
                    'status_detail': mp_payment['status_detail'],
                    'payment_method': mp_payment['payment_method_id'],
                    'transaction_amount': mp_payment['transaction_amount'],
                    'last_updated': mp_payment['last_updated']
                }
            
            return {'error': 'Erro ao consultar status do pagamento'}
        except Exception as e:
            return {'error': str(e)} 