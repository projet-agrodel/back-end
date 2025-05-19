import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from unittest.mock import patch

class OrderRoutesTest(unittest.TestCase):

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
        
        # Criar um pedido para teste
        pedido = Order(user_id=1, description="Pedido de teste", amount=300.00)
        db.session.add(pedido)
        
        db.session.commit()

    # Mock para simular JWT token identity
    def get_jwt_identity_mock(self, return_value=1):
        return patch('app.routes.order_routes.get_jwt_identity', return_value=return_value)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_criar_pedido_sucesso(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/orders', json={
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ],
                "description": "Novo pedido de teste"
            })
            
            self.assertEqual(response.status_code, 201)
            self.assertIn("Pedido criado com sucesso", response.get_json()["message"])

    def test_criar_pedido_sem_estoque(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/orders', json={
                "items": [
                    {"product_id": 1, "quantity": 100}  # Quantidade maior que o estoque
                ],
                "description": "Pedido sem estoque"
            })
            
            self.assertEqual(response.status_code, 400)

    def test_listar_pedidos_usuario(self):
        with self.get_jwt_identity_mock():
            response = self.client.get('/orders')
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)

    def test_obter_detalhes_pedido(self):
        with self.get_jwt_identity_mock():
            response = self.client.get('/orders/1')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 1)

    def test_obter_pedido_inexistente(self):
        with self.get_jwt_identity_mock():
            response = self.client.get('/orders/9999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn("Pedido não encontrado", response.get_json()["message"])

if __name__ == '__main__':
    unittest.main() 