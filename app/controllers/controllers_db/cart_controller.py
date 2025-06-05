from typing import List, Optional, Dict
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.controllers.base.base_controller import BaseController
from ..base.main_controller import MainController

class CartController(BaseController[Cart]):
    def __init__(self, client: MainController) -> None:
        super().__init__(Cart, client)

    def get_or_create_cart(self, user_id: int) -> Cart:
        cart = self.get_query().filter_by(user_id=user_id).first()
        if not cart:
            cart = self.create({'user_id': user_id})
        return cart

    def add_item(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        try:
            cart = self.get_or_create_cart(user_id)
            product = Product.query.get_or_404(product_id)
            
            if product.stock < quantity:
                raise ValueError("Quantidade solicitada maior que estoque disponível")
            
            cart_item = CartItem.query.filter_by(
                carrinho_id=cart.id,
                produto_id=product_id
            ).first()
            
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(
                    carrinho_id=cart.id,
                    produto_id=product_id,
                    quantity=quantity
                )
                self._db.session.add(cart_item)
            
            self._db.session.commit()
            return cart_item
        except Exception as e:
            self._db.session.rollback()
            raise e

    def remove_item(self, user_id: int, product_id: int) -> bool:
        try:
            cart = self.get_query().filter_by(user_id=user_id).first()
            if not cart:
                raise ValueError("Carrinho não encontrado")
            
            cart_item = CartItem.query.filter_by(
                carrinho_id=cart.id,
                produto_id=product_id
            ).first()
            
            if cart_item:
                self._db.session.delete(cart_item)
                self._db.session.commit()
                return True
            return False
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_cart_items(self, user_id: int) -> List[CartItem]:
        cart = self.get_query().filter_by(user_id=user_id).first()
        if not cart:
            return []
        return cart.items 

    def sync_cart(self, user_id: int, cart_items: List[Dict]) -> List[CartItem]:
        try:
            # Obter ou criar o carrinho do usuário
            cart = self.get_or_create_cart(user_id)
            
            # Se quiser mesclar os carrinhos, remova esta linha
            CartItem.query.filter_by(carrinho_id=cart.id).delete()
            
            # Adicionar os novos itens do carrinho local
            synced_items = []
            for item in cart_items:
                produto_id = item.get('produto_id')
                quantity = item.get('quantity', 1)

                product = Product.query.get(produto_id)
                if not product:
                    continue  # Ignorar produtos que não existem mais

                if product.status != 'Ativo':
                    continue
                    
                adjusted_quantity = min(quantity, product.stock)
                if adjusted_quantity <= 0:
                    continue  # Pular se não houver estoque
                
                # Criar o item no carrinho
                cart_item = CartItem(
                    carrinho_id=cart.id,
                    produto_id=produto_id,
                    quantity=adjusted_quantity
                )
                self._db.session.add(cart_item)
                synced_items.append(cart_item)
            
            self._db.session.commit()
            
            return self.get_cart_items(user_id)
            
        except Exception as e:
            self._db.session.rollback()
            raise e 