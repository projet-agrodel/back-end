from typing import List, Optional
from app.models.product import Product
from app.controllers.base.base_controller import BaseController
from decimal import Decimal

class ProductController(BaseController[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

    def create_product(self, data: dict) -> Product:
        try:
            return self.create({
                'name': data['name'],
                'description': data.get('description'),
                'price': Decimal(str(data['price'])),
                'stock': data['stock']
            })
        except Exception as e:
            self._db.session.rollback()
            raise e

    def update_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        try:
            product = self.get_by_id(product_id)
            if product:
                product.stock += quantity
                self._db.session.commit()
                return product
            return None
        except Exception as e:
            self._db.session.rollback()
            raise e

    def search_products(self, query: str) -> List[Product]:
        return self.get_query().filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        ).all()

    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        return self.get_query().filter(
            Product.price.between(min_price, max_price)
        ).all()

    def get_products_in_stock(self) -> List[Product]:
        return self.get_query().filter(Product.stock > 0).all()

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        return self.get_query().filter(Product.stock <= threshold).all()

    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        product = self.get_by_id(product_id)
        return product is not None and product.stock >= quantity 