from typing import List, Optional, Dict
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User
from app.controllers.base.base_controller import BaseController
from decimal import Decimal
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from ..base.main_controller import MainController

class OrderController(BaseController[Order]):
    def __init__(self, client: MainController) -> None:
        super().__init__(Order, client)

    def get_all(self) -> List[Order]:
        return self.get_query().options(
            joinedload(Order.user),
            joinedload(Order.items).joinedload(OrderItem.product)
        ).all()

    def create_order(self, user_id: int, items: List[Dict], description: bytes) -> Order:
        try:
            total_amount = Decimal('0.0')
            order_items = []

            for item in items:
                product = Product.query.get_or_404(item['produto_id'])

                if product.stock < item['quantity']:
                    raise ValueError(f"Produto {product.name} sem estoque suficiente")
                
                item_amount = product.price * Decimal(str(item['quantity']))
                total_amount += item_amount
                order_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'amount': product.price
                })

            order = self.create({
                'user_id': int(user_id),
                'description': description,
                'amount': total_amount,
                'status': OrderStatus.EM_PROCESSAMENTO
            })

            for item in order_items:
                order_item = OrderItem(
                    pedido_id=order.id,
                    produto_id=item['product'].id,
                    quantity=item['quantity'],
                    price=item['amount']
                )
                self._db.session.add(order_item)
                item['product'].stock -= item['quantity']

            self._db.session.commit()
            return order
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_user_orders(self, user_id: int) -> List[Order]:
        return self.get_query().filter_by(user_id=user_id).all()

    def get_order_with_items(self, order_id: int) -> Optional[Order]:
        return self.get_query().filter_by(id=order_id).first()

    def get_order_with_items_and_check_permission(self, order_id: int, user_id: int, is_admin: bool = False) -> Optional[Order]:
        order = self.get_order_with_items(order_id)
        if not order:
            return None
        if not is_admin and order.user_id != user_id:
            raise PermissionError("Você não tem permissão para acessar este pedido")
        return order

    def update_order_status(self, order_id: int, status: str, user_id: int, is_admin: bool = False) -> Optional[Order]:
        try:
            order = self.get_order_with_items_and_check_permission(order_id, user_id, is_admin)
            if not order:
                return None
                
            try:
                new_status = OrderStatus(status)
            except ValueError:
                valid_statuses = [status.value for status in OrderStatus]
                raise ValueError(f"Status inválido. Status permitidos: {', '.join(valid_statuses)}")
                
            order.status = new_status
            self._db.session.commit()
            return order
        except Exception as e:
            self._db.session.rollback()
            raise e

    def search_orders(self, 
                     user_id: Optional[int] = None,
                     status: Optional[str] = None,
                     search_term: Optional[str] = None,
                     is_admin: bool = False) -> List[Order]:
        query = self.get_query()
        
        # Se não for admin, filtrar apenas pedidos do usuário
        if not is_admin:
            if user_id is None:
                raise ValueError("ID do usuário é obrigatório para usuários não administradores")
            query = query.filter_by(user_id=user_id)
        elif user_id is not None:
            query = query.filter_by(user_id=user_id)
            
        if status and status != 'Todos':
            try:
                query = query.filter_by(status=OrderStatus(status))
            except ValueError:
                valid_statuses = [status.value for status in OrderStatus]
                raise ValueError(f"Status inválido. Status permitidos: {', '.join(valid_statuses)}")
            
        if search_term:
            search = f"%{search_term}%"
            query = query.join(Order.user).filter(
                or_(
                    Order.description.ilike(search) if isinstance(Order.description, str) else Order.description.cast(str).ilike(search),
                    User.name.ilike(search)
                )
            )
            
        return query.all()

    def delete_order(self, order_id: int, user_id: int, is_admin: bool = False) -> bool:
        try:
            order = self.get_order_with_items_and_check_permission(order_id, user_id, is_admin)
            if not order:
                return False
                
            # Devolver os produtos ao estoque
            for item in order.items:
                item.product.stock += item.quantity
                
            self._db.session.delete(order)
            self._db.session.commit()
            return True
        except Exception as e:
            self._db.session.rollback()
            raise e 
    
    def update_status_by_api_payament(self, order_id):
        order = self.get_order_with_items(order_id)      

        if len(order.payments) == 0:
            return None
        
        payment = order.payments[0]

        details = self.client.payments.check_payment_status(payment.transaction_id)

        return details

        status_mapping = {
            'approved': 'Aprovado',
            'pending': 'Pendente',
            'in_process': 'Em Processamento',
            'rejected': 'Rejeitado',
            'cancelled': 'Cancelado',
            'refunded': 'Reembolsado'
        }
