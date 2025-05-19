import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from unittest.mock import patch

class CartRoutesTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            cls.inserir_dados_fixos()

    @classmethod
    def tearDown(cls):
        with cls.app.app_context():
            db.drop_all()
            db.session.remove()

    @classmethod
    def inserir_dados_fixos(cls):
        # Criar usuário para teste
        usuario = User(name="Cliente Teste", email="cliente@email.com", password="senha123", phone="11987654321", type="user")
        db.session.add(usuario)
        
        # Criar produtos para teste
        produtos = [
            Product(name="Produto A", description="Descrição A", price=100.00, stock=20),
            Product(name="Produto B", description="Descrição B", price=200.00, stock=15)
        ]
        db.session.add_all(produtos)
        
        # Criar carrinho para teste
        carrinho = Cart(user_id=1)
        db.session.add(carrinho)
        
        # Adicionar item ao carrinho
        item_carrinho = CartItem(carrinho_id=1, produto_id=1, quantity=3)
        db.session.add(item_carrinho)
        
        db.session.commit()

    # Mock para simular JWT token identity
    def get_jwt_identity_mock(self, return_value=1):
        return patch('app.routes.cart_routes.get_jwt_identity', return_value=return_value)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_obter_carrinho(self):
        with self.get_jwt_identity_mock():
            response = self.client.get('/cart')
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)
            
    def test_adicionar_item_carrinho_sucesso(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/cart/add', json={
                "product_id": 2,
                "quantity": 2
            })
            
            self.assertEqual(response.status_code, 201)
            self.assertIn("Item adicionado ao carrinho com sucesso", response.get_json()["message"])
    
    def test_adicionar_item_carrinho_sem_produto(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/cart/add', json={
                "quantity": 2
            })
            
            self.assertEqual(response.status_code, 400)
            self.assertIn("ID do produto é obrigatório", response.get_json()["message"])
    
    def test_adicionar_item_carrinho_sem_estoque(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/cart/add', json={
                "product_id": 1,
                "quantity": 100  # Quantidade maior que o estoque
            })
            
            self.assertEqual(response.status_code, 400)
    
    def test_remover_item_carrinho_sucesso(self):
        with self.get_jwt_identity_mock():
            response = self.client.delete('/cart/remove/1')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("Item removido do carrinho com sucesso", response.get_json()["message"])
    
    def test_remover_item_carrinho_inexistente(self):
        with self.get_jwt_identity_mock():
            response = self.client.delete('/cart/remove/9999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn("Item não encontrado no carrinho", response.get_json()["message"])

if __name__ == '__main__':
    unittest.main() 