from flask_jwt_extended import create_access_token
from app.models.product import Product
import json

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