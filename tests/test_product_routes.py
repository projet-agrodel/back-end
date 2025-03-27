import unittest
from app import create_app, db
from app.models.user import User
from app.models.product import Product

class ProductRoutesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')  # Configuração específica para testes
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()
            cls.inserir_dados_fixos()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    @classmethod
    def inserir_dados_fixos(cls):
        admin = User(name="Admin", email="admin@email.com", password="admin123", phone="11999999999", salt="123", type="admin")
        db.session.add(admin)
        db.session.commit()

        produtos = [
            Product(name="Teclado Mecânico", description="Teclado RGB", price=299.99, stock=50),
            Product(name="Mouse Gamer", description="Mouse óptico", price=199.99, stock=30)
        ]
        db.session.add_all(produtos)
        db.session.commit()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_criar_produto_sucesso(self):
        response = self.client.post('/products', json={
            "name": "Monitor 144Hz",
            "description": "Monitor Full HD 144Hz",
            "price": 1299.99,
            "stock": 10
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Monitor 144Hz", response.get_json()['name'])

    def test_criar_produto_faltando_dados(self):
        response = self.client.post('/products', json={
            "name": "Mousepad"
        })
        self.assertEqual(response.status_code, 400)

    def test_listar_produtos(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)

    def test_buscar_produto_existente(self):
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Teclado Mecânico")

    def test_buscar_produto_inexistente(self):
        response = self.client.get('/products/9999')
        self.assertEqual(response.status_code, 404)

    def test_atualizar_produto_sucesso(self):
        response = self.client.put('/products/1', json={"name": "Teclado RGB Atualizado"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Teclado RGB Atualizado")

    def test_atualizar_produto_inexistente(self):
        response = self.client.put('/products/9999', json={"name": "Novo Nome"})
        self.assertEqual(response.status_code, 404)

    def test_atualizar_estoque_sucesso(self):
        response = self.client.patch('/products/1/stock', json={"quantity": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["stock"], 55)

    def test_atualizar_estoque_invalido(self):
        response = self.client.patch('/products/1/stock', json={"quantity": "abc"})
        self.assertEqual(response.status_code, 400)

    def test_deletar_produto_sucesso(self):
        response = self.client.delete('/products/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Produto deletado com sucesso", response.get_json()["message"])

    def test_deletar_produto_inexistente(self):
        response = self.client.delete('/products/9999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
