from typing import List, Optional, Dict
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.controllers.base.base_controller import BaseController
from decimal import Decimal

class OrderController(BaseController[Order]):
    def __init__(self) -> None:
        super().__init__(Order)

    def create_order(self, user_id: int, items: List[Dict], description: bytes) -> Order:
        try:
            total_amount = Decimal('0.0')
            order_items = []

            for item in items:
                product = Product.query.get_or_404(item['product_id'])
                if product.stock < item['quantity']:
                    raise ValueError(f"Produto {product.name} sem estoque suficiente")
                
                total_amount += product.price * Decimal(str(item['quantity']))
                order_items.append({
                    'product': product,
                    'quantity': item['quantity']
                })

            order = self.create({
                'user_id': user_id,
                'description': description,
                'amount': total_amount
            })

            for item in order_items:
                order_item = OrderItem(
                    pedido_id=order.id,
                    produto_id=item['product'].id,
                    quantity=item['quantity']
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