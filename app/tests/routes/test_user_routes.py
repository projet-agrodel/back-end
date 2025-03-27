import unittest
import json
from app import create_app, db
from app.models.user import User

class UserRoutesTest(unittest.TestCase):

    @classmethod
    def setUp(cls):    
        cls.app = create_app()  # Configuração específica para testes
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
        admin = User(name="Admin", email="admin@email.com", password="admin123", phone="11999999999", type="admin")
        user = User(name="User", email="user@email.com", password="user123", phone="11888888888", type="user")
        db.session.add_all([admin, user])
        db.session.commit()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------

    def test_criar_usuario_sucesso(self):    
        response = self.client.post('/users', json={
            "name": "Novo Usuário",
            "email": "novo@email.com",
            "password": "senha123",
            "phone": "11912345678",
            "type": "user"
        })

        self.assertIn("Usuário criado com sucesso", response.get_json()["message"])
        self.assertEqual(response.status_code, 201)

    def test_criar_usuario_faltando_dados(self):    
        response = self.client.post('/users', json={
            "name": "Usuário Incompleto"
        })
        self.assertEqual(response.status_code, 400)

    def test_listar_usuarios(self):    
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)

    def test_buscar_usuario_existente(self):    
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Admin")

    def test_buscar_usuario_inexistente(self):    
        response = self.client.get('/users/9999')
        self.assertEqual(response.status_code, 404)

    def test_atualizar_usuario_sucesso(self):    
        response = self.client.put('/users/1', json={"name": "Admin Atualizado"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário atualizado com sucesso", response.get_json()["message"])

    def test_atualizar_usuario_inexistente(self):    
        response = self.client.put('/users/9999', json={"name": "Nome Inexistente"})
        self.assertEqual(response.status_code, 404)

    def test_deletar_usuario_sucesso(self):    
        response = self.client.delete('/users/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuário deletado com sucesso", response.get_json()["message"])

    def test_deletar_usuario_inexistente(self):    
        response = self.client.delete('/users/9999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
