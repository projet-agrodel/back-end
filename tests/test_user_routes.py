from flask_jwt_extended import create_access_token
from app.models.user import User
import json

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

def test_get_users(client, admin_token):
    response = client.get('/users', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list) 