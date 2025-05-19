import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.order import Order
from app.models.payment import Payment
from unittest.mock import patch
from decimal import Decimal

class PaymentRoutesTest(unittest.TestCase):

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
        admin = User(name="Admin Teste", email="admin@email.com", password="admin123", phone="11999999999", type="admin")
        db.session.add_all([usuario, admin])
        
        # Criar pedido para teste
        pedido = Order(user_id=1, description="Pedido de teste", amount=300.00)
        db.session.add(pedido)
        
        # Criar pagamento para teste
        pagamento = Payment(
            pedido_id=1,
            payment_method="Cartão de Crédito",
            status="Pendente",
            amount=300.00,
            transaction_id="tx_12345"
        )
        db.session.add(pagamento)
        
        db.session.commit()

    # Mock para simular decoradores de autenticação e autorização
    def admin_required_mock(self):
        return patch('app.routes.payment_routes.admin_required', lambda f: f)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_criar_pagamento_sucesso(self):
        response = self.client.post('/payments', json={
            "order_id": 1,
            "payment_method": "Boleto",
            "amount": 300.00,
            "transaction_id": "tx_67890"
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("Pagamento registrado com sucesso", response.get_json()["message"])

    def test_criar_pagamento_valor_incorreto(self):
        response = self.client.post('/payments', json={
            "order_id": 1,
            "payment_method": "Boleto",
            "amount": 200.00,  # Valor diferente do pedido
            "transaction_id": "tx_67890"
        })
        
        self.assertEqual(response.status_code, 400)

    def test_listar_pagamentos_pedido(self):
        response = self.client.get('/payments/order/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)
        self.assertEqual(response.get_json()[0]["pedido_id"], 1)

    def test_atualizar_status_pagamento(self):
        with self.admin_required_mock():
            response = self.client.put('/payments/1/status', json={
                "status": "Aprovado"
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("Status do pagamento atualizado com sucesso", response.get_json()["message"])
            self.assertEqual(response.get_json()["status"], "Aprovado")

    def test_atualizar_status_pagamento_sem_status(self):
        with self.admin_required_mock():
            response = self.client.put('/payments/1/status', json={})
            
            self.assertEqual(response.status_code, 400)
            self.assertIn("Status é obrigatório", response.get_json()["message"])

    def test_atualizar_status_pagamento_inexistente(self):
        with self.admin_required_mock():
            response = self.client.put('/payments/9999/status', json={
                "status": "Aprovado"
            })
            
            self.assertEqual(response.status_code, 404)
            self.assertIn("Pagamento não encontrado", response.get_json()["message"])

    def test_listar_pagamentos_pendentes(self):
        with self.admin_required_mock():
            response = self.client.get('/payments/pending')
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)
            self.assertEqual(response.get_json()[0]["status"], "Pendente")

if __name__ == '__main__':
    unittest.main() 