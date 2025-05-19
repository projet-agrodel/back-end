from typing import List, Optional
from ...models.product import Product
from ..base.base_controller import BaseController
from ...extensions import db
from sqlalchemy import or_, asc, desc
from decimal import Decimal
# from ...models.category import Category # Não é estritamente necessário para este filtro simples

class ProductController(BaseController[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

    def create_product(self, data: dict) -> Product:
        try:
            if 'price' in data and data['price'] is not None:
                try:
                    data['price'] = Decimal(str(data['price']))
                except Exception as e:
                    pass 
            
            if 'originalPrice' in data and data['originalPrice'] is not None:
                try:
                    data['originalPrice'] = Decimal(str(data['originalPrice']))
                except Exception as e:
                    pass 

            if 'isPromotion' in data and not isinstance(data['isPromotion'], bool):
                data['isPromotion'] = str(data['isPromotion']).lower() in ['true', '1', 't']

            if 'status' in data and data['status'] not in ['Ativo', 'Inativo']:
                if not isinstance(data['status'], str) or data['status'] not in ['Ativo', 'Inativo']:
                     data.pop('status', None)

            new_product = self.create(data) # self.create é do BaseController e já faz commit
            return new_product
        except Exception as e:
            self._db.session.rollback()
            raise e

    def update_product(self, product_id: int, data: dict) -> Optional[Product]:
        try:
            product = self.get_by_id(product_id)
            if not product:
                return None

            if 'price' in data and data['price'] is not None:
                try:
                    product.price = Decimal(str(data['price']))
                except Exception as e:
                    # Considerar levantar um erro se a conversão falhar
                    pass # ou raise ValueError(f"Valor inválido para preço: {data['price']}")
            elif 'price' in data and data['price'] is None:
                product.price = None # Permitir definir o preço como nulo se o modelo permitir

            if 'originalPrice' in data and data['originalPrice'] is not None:
                try:
                    product.originalPrice = Decimal(str(data['originalPrice']))
                except Exception as e:
                    pass
            elif 'originalPrice' in data and data['originalPrice'] is None:
                product.originalPrice = None

            if 'isPromotion' in data:
                if isinstance(data['isPromotion'], bool):
                    product.isPromotion = data['isPromotion']
                else:
                    product.isPromotion = str(data['isPromotion']).lower() in ['true', '1', 't']
            
            if 'status' in data and data['status'] is not None:
                if data['status'] in ['Ativo', 'Inativo']:
                    product.status = data['status']
                else:
                    pass 
            elif 'status' in data and data['status'] is None:
                 pass

            # Para outros campos que não precisam de tratamento especial:
            allowed_fields = ['name', 'description', 'stock', 'category_id', 'imageUrl'] 
            for field in allowed_fields:
                if field in data:
                    setattr(product, field, data[field])
            
            self._db.session.commit() # ADICIONAR ESTA LINHA para persistir as alterações
            return product
        except Exception as e:
            self._db.session.rollback()
            raise e


    def get_all(self, query: str = None, min_price: float = None, max_price: float = None, sort: str = None, status: str = None, for_admin: bool = False) -> List[Product]:
        base_query = self.get_query()
        
        if query:
            search_term = f'%{query}%'
            base_query = base_query.filter(or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            ))

        if status is not None:
            base_query = base_query.filter(Product.status == status)
            
        if min_price is not None:
            try:
                min_price_decimal = Decimal(str(min_price))
                base_query = base_query.filter(Product.price >= min_price_decimal)
            except (ValueError, TypeError):
                pass # Ignorar filtro se o valor for inválido

        if max_price is not None:
            try:
                max_price_decimal = Decimal(str(max_price))
                base_query = base_query.filter(Product.price <= max_price_decimal)
            except (ValueError, TypeError):
                pass # Ignorar filtro se o valor for inválido
        
        # Filtro de status
        if not for_admin: # Se não for para admin, aplicar filtro de status padrão 'Ativo'
            # Se um status específico for passado E não for para admin, usar esse status.
            # Caso contrário, se for para admin, o filtro de status abaixo (status explícito) pode ser usado.
            # Ou seja, para usuários, se `status` não for passado, assume 'Ativo'.
            # Se `status` for passado (e.g. 'Inativo') por um usuário, ele não verá nada se não for 'Ativo'
            # A lógica aqui é que `for_admin=False` sempre tentará impor 'Ativo' a menos que `status` seja explicitamente `Ativo`.
            # Melhor: Se não for admin, só mostrar ativos. Se for admin, permitir filtrar por status.
            base_query = base_query.filter(Product.status == 'Ativo')
        elif status: # Se for para admin E um status específico foi solicitado
            base_query = base_query.filter(Product.status == status)
        # Se for_admin e nenhum status específico, retorna todos os status.
                
        if sort:
            if sort == 'price_asc':
                base_query = base_query.order_by(asc(Product.price))
            elif sort == 'price_desc':
                base_query = base_query.order_by(desc(Product.price))

            # Adicionar mais opções de sort se necessário (ex: nome, data)

        return base_query.all()

    def update_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        if product.stock + quantity < 0:
            raise ValueError("Estoque não pode ser negativo")
            
        product.stock += quantity
        self._db.session.commit()
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