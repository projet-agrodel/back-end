import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.card import Card
from unittest.mock import patch, MagicMock

class CardRoutesTest(unittest.TestCase):

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
        
        # Um cartão de crédito já existente
        # Na aplicação real seria criptografado
        cartao = Card(
            user_id=1,
            card_number="4111111111111111",
            card_holder_name="CLIENTE TESTE",
            card_expiration_date="12/25",
            card_cvv="123"
        )
        db.session.add(cartao)
        
        db.session.commit()

    # Mock para simular JWT token identity
    def get_jwt_identity_mock(self, return_value=1):
        return patch('app.routes.card_routes.get_jwt_identity', return_value=return_value)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_criar_cartao_sucesso(self):
        with self.get_jwt_identity_mock():
            response = self.client.post('/cards', json={
                "card_number": "5111111111111118",
                "card_holder_name": "CLIENTE TESTE",
                "card_expiration_date": "10/28",
                "card_cvv": "456"
            })
            
            self.assertEqual(response.status_code, 201)
            self.assertIn("Cartão adicionado com sucesso", response.get_json()["message"])

    @patch('app.controllers.controllers_db.card_controller.EncryptionService')
    def test_listar_cartoes_usuario(self, mock_encryption):
        # Configure o mock para retornar valores simulados
        instance = mock_encryption.return_value
        instance.decrypt.return_value = "4111111111111111"
        
        with self.get_jwt_identity_mock(), \
             patch('app.routes.card_routes.controller.cards.encryption_service', instance):
            response = self.client.get('/cards')
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)
            self.assertEqual(response.get_json()[0]["card_holder_name"], "CLIENTE TESTE")

    @patch('app.controllers.controllers_db.card_controller.EncryptionService')
    def test_obter_detalhes_cartao(self, mock_encryption):
        # Configure o mock para retornar valores simulados
        instance = mock_encryption.return_value
        instance.decrypt.return_value = "4111111111111111"
        
        with self.get_jwt_identity_mock(), \
             patch('app.routes.card_routes.controller.cards.encryption_service', instance), \
             patch('app.controllers.controllers_db.card_controller.CardController.get_card_details') as mock_get_details:
            
            # Simular resposta do método get_card_details
            mock_get_details.return_value = {
                'id': 1,
                'card_holder_name': 'CLIENTE TESTE',
                'card_number': '1111',
                'expiration_date': '2025-12-01'
            }
            
            response = self.client.get('/cards/1')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 1)
            self.assertEqual(response.get_json()["card_holder_name"], "CLIENTE TESTE")

    def test_obter_cartao_inexistente(self):
        with self.get_jwt_identity_mock(), \
             patch('app.controllers.controllers_db.card_controller.CardController.get_card_details') as mock_get_details:
            
            # Simular cartão não encontrado
            mock_get_details.return_value = None
            
            response = self.client.get('/cards/9999')
            
            self.assertEqual(response.status_code, 404)
            self.assertIn("Cartão não encontrado", response.get_json()["message"])

if __name__ == '__main__':
    unittest.main() 