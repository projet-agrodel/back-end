import pytest
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from flask_jwt_extended import create_access_token
import json

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app):
    with app.app_context():
        admin = User(
            name='Admin',
            email='admin@test.com',
            password='hashed_password',
            salt='salt',
            type='admin'
        )
        db.session.add(admin)
        db.session.commit()
        
        return create_access_token(identity=admin.id)

def test_create_product(client, admin_token):
    response = client.post(
        '/products',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 99.99,
            'stock': 10
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Product'

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_create_user(client, admin_token):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test User',
            'email': 'test@test.com',
            'password': 'password123',
            'phone': '1234567890',
            'type': 'client'
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data

# Adicione mais testes conforme necessário 