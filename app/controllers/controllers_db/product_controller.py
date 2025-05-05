from typing import List, Optional
from ...models.product import Product
from ..base.base_controller import BaseController
from ...extensions import db
from sqlalchemy import or_, asc, desc
from decimal import Decimal

class ProductController(BaseController[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

    def create_product(self, data: dict) -> Product:
        try:
            if 'price' in data:
                data['price'] = Decimal(str(data['price']))
                
            new_product = self.create(data)
            return new_product
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_all(self, query: str = None, min_price: float = None, max_price: float = None, sort: str = None) -> List[Product]:
        base_query = self.get_query()
        
        if query:
            search_term = f'%{query}%'
            base_query = base_query.filter(or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            ))
            
        if min_price is not None:
            try:
                min_price_decimal = Decimal(str(min_price))
                base_query = base_query.filter(Product.price >= min_price_decimal)
            except (ValueError, TypeError):
                pass

        if max_price is not None:
            try:
                max_price_decimal = Decimal(str(max_price))
                base_query = base_query.filter(Product.price <= max_price_decimal)
            except (ValueError, TypeError):
                pass
                
        if sort:
            if sort == 'price_asc':
                base_query = base_query.order_by(asc(Product.price))
            elif sort == 'price_desc':
                base_query = base_query.order_by(desc(Product.price))

        return base_query.all()

    def update_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        if product.stock + quantity < 0:
            raise ValueError("Estoque não pode ser negativo")
            
        product.stock += quantity
        self.save(product)
        return product

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